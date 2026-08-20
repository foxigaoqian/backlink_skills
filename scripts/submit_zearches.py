#!/usr/bin/env python3
"""Submit one approved website to Zearches through its normal public form.

This adapter intentionally does not bypass CAPTCHAs, login walls, email checks,
or other safeguards. It performs at most one final POST per invocation.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, build_opener

SUBMIT_PAGE = "https://zearches.com/submit-website-free.php"
USER_AGENT = "Mozilla/5.0 (compatible; BacklinkSkills/1.0; +https://github.com/foxigaoqian/backlink_skills)"


class FormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.forms: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.current_select: dict[str, Any] | None = None
        self.current_option: dict[str, Any] | None = None

    @staticmethod
    def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {k.lower(): (v or "") for k, v in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = self.attrs_dict(attrs)
        tag = tag.lower()
        if tag == "form":
            self.current = {
                "action": a.get("action", ""),
                "method": a.get("method", "post").lower(),
                "inputs": [],
                "textareas": [],
                "selects": [],
            }
            return
        if self.current is None:
            return
        if tag == "input":
            self.current["inputs"].append(a)
        elif tag == "textarea":
            self.current["textareas"].append(a)
        elif tag == "select":
            self.current_select = {"attrs": a, "options": []}
            self.current["selects"].append(self.current_select)
        elif tag == "option" and self.current_select is not None:
            self.current_option = {"attrs": a, "text": ""}
            self.current_select["options"].append(self.current_option)

    def handle_data(self, data: str) -> None:
        if self.current_option is not None:
            self.current_option["text"] += data

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "option":
            self.current_option = None
        elif tag == "select":
            self.current_select = None
            self.current_option = None
        elif tag == "form" and self.current is not None:
            self.forms.append(self.current)
            self.current = None
            self.current_select = None
            self.current_option = None


def fetch(url: str) -> tuple[str, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    with build_opener().open(req, timeout=30) as resp:
        return resp.geturl(), resp.read().decode("utf-8", errors="replace")


def choose_form(forms: list[dict[str, Any]]) -> dict[str, Any]:
    scored: list[tuple[int, dict[str, Any]]] = []
    for form in forms:
        score = 0
        for inp in form["inputs"]:
            name = inp.get("name", "").lower()
            ph = inp.get("placeholder", "").lower()
            if "https://" in ph or "url" in name:
                score += 5
            if "title" in name or "title" in ph:
                score += 3
        for ta in form["textareas"]:
            if "desc" in ta.get("name", "").lower():
                score += 3
        for sel in form["selects"]:
            option_text = " ".join(o.get("text", "") for o in sel["options"]).lower()
            if "gaming" in option_text or "esports" in option_text:
                score += 5
        scored.append((score, form))
    if not scored:
        raise RuntimeError("No HTML forms found on submission page")
    score, form = max(scored, key=lambda x: x[0])
    if score < 5:
        raise RuntimeError("Could not confidently identify the Zearches submission form")
    return form


def set_first(payload: dict[str, str], candidates: list[dict[str, str]], value: str, *, role: str) -> str | None:
    for inp in candidates:
        name = inp.get("name", "")
        if not name:
            continue
        lname = name.lower()
        ph = inp.get("placeholder", "").lower()
        typ = inp.get("type", "text").lower()
        if typ in {"hidden", "submit", "button", "checkbox", "radio", "file"}:
            continue
        if role == "url" and ("url" in lname or "https://" in ph):
            payload[name] = value
            return name
        if role == "title" and ("title" in lname or "title" in ph):
            payload[name] = value
            return name
    return None


def build_payload(form: dict[str, Any], request_data: dict[str, Any]) -> dict[str, str]:
    payload: dict[str, str] = {}

    # Preserve server-provided hidden fields such as CSRF/nonces.
    for inp in form["inputs"]:
        if inp.get("type", "").lower() == "hidden" and inp.get("name"):
            payload[inp["name"]] = inp.get("value", "")

    url_name = set_first(payload, form["inputs"], request_data["url"], role="url")
    title_name = set_first(payload, form["inputs"], request_data["title"], role="title")
    if not url_name:
        raise RuntimeError("Could not locate the URL field")
    if not title_name:
        raise RuntimeError("Could not locate the title field")

    # Description textarea.
    desc_name = None
    for ta in form["textareas"]:
        name = ta.get("name", "")
        if name and ("desc" in name.lower() or not desc_name):
            desc_name = name
            if "desc" in name.lower():
                break
    if not desc_name:
        raise RuntimeError("Could not locate the description field")
    payload[desc_name] = request_data["description"]

    # Category select: prefer exact/partial keyword matches from the approved request.
    category_keywords = [x.lower() for x in request_data.get("category_keywords", ["Gaming & Esports", "Gaming", "Games"])]
    category_set = False
    for sel in form["selects"]:
        name = sel["attrs"].get("name", "")
        if not name:
            continue
        for keyword in category_keywords:
            for option in sel["options"]:
                text = re.sub(r"\s+", " ", option.get("text", "")).strip()
                if keyword in text.lower():
                    payload[name] = option["attrs"].get("value", text)
                    category_set = True
                    break
            if category_set:
                break
        if category_set:
            break
    if not category_set:
        raise RuntimeError("Could not find an approved gaming category; refusing generic-category fallback")

    # Explicitly keep common honeypot names blank. Do not populate unidentified fields.
    for inp in form["inputs"]:
        name = inp.get("name", "")
        if not name or name in payload:
            continue
        lname = name.lower()
        if lname in {"website", "website2", "homepage2", "company_website"}:
            payload[name] = ""

    return payload


def encode_form(payload: dict[str, str]) -> bytes:
    from urllib.parse import urlencode
    return urlencode(payload).encode("utf-8")


def submit(request_path: Path) -> int:
    data = json.loads(request_path.read_text(encoding="utf-8"))
    required = ["url", "title", "description"]
    missing = [k for k in required if not isinstance(data.get(k), str) or not data[k].strip()]
    if missing:
        raise RuntimeError(f"Missing required request fields: {', '.join(missing)}")

    landing_url, html = fetch(SUBMIT_PAGE)
    parser = FormParser()
    parser.feed(html)
    form = choose_form(parser.forms)
    payload = build_payload(form, data)

    action = urljoin(landing_url, form.get("action") or landing_url)
    method = (form.get("method") or "post").lower()
    if method != "post":
        raise RuntimeError(f"Unexpected form method {method!r}; refusing to guess")

    print(f"Submitting one approved listing to: {action}")
    print(f"Target: {data['url']}")
    print(f"Title: {data['title']}")
    print("Final POST attempts: 1")

    req = Request(
        action,
        data=encode_form(payload),
        method="POST",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": landing_url,
        },
    )

    try:
        with build_opener().open(req, timeout=30) as resp:
            final_url = resp.geturl()
            body = resp.read().decode("utf-8", errors="replace")
            status = getattr(resp, "status", 200)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP error on final POST: {exc.code}")
        print(re.sub(r"\s+", " ", body)[:800])
        return 4
    except URLError as exc:
        print(f"Network error on final POST: {exc}")
        return 5

    normalized = re.sub(r"\s+", " ", body).lower()
    domain = re.sub(r"^https?://(www\.)?", "", data["url"]).split("/", 1)[0].lower()
    positive_terms = ("thank", "success", "submitted", "listing", "saved", "added", "latest submissions")
    evidence = domain in normalized and any(term in normalized for term in positive_terms)

    print(f"Response status: {status}")
    print(f"Response URL: {final_url}")
    print("Response excerpt:")
    print(re.sub(r"\s+", " ", body)[:1200])

    if evidence:
        print("RESULT: submitted — response contains the target domain and positive submission evidence")
        return 0

    # A 2xx response alone is not enough to claim success.
    print("RESULT: submission outcome unknown — no reliable success evidence found; do not retry automatically")
    return 3


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} path/to/request.json", file=sys.stderr)
        return 2
    try:
        return submit(Path(sys.argv[1]))
    except Exception as exc:  # noqa: BLE001 - CLI should report controlled failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
