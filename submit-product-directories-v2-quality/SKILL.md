---
name: submit-product-directories-v2-quality
description: SPD V2 Quality. Discover, deeply qualify, submit, and audit truthful listings across Windows, macOS, and Linux-capable environments with audience-value screening, SEO quality gates, browser-first execution, action-level authorization, privacy controls, and evidence-backed records. Use when listing quality, referral value, governance, durability, and auditable compliance matter more than submission volume. Do not use for bulk backlink spam, ranking manipulation, guest-post automation, mass email, paid link acquisition, or automatic submission to low-quality directories.
---

# SPD V2 Quality — quality-oriented directory discovery and submission

## Version identity

- Canonical name: `SPD V2 Quality`.
- Invocation: `$submit-product-directories-v2-quality`.
- Optimize for audience relevance, discovery value, governance, referral potential, listing durability, and evidence quality.
- Use when quality and long-term value matter more than queue throughput.
- Route large preapproved source lists whose primary need is operational throughput to `$submit-product-directories-v1-batch`.
- Do not call this version `SPD V1`, `SPD Batch`, or generic `SPD` in records.
- Treat records without an explicit version as legacy until they pass the V2 auditor.

Run directory discovery and listing work as a compliance-gated state machine. Optimize for product/project discovery, accurate public profiles, qualified referral traffic, and durable listings—not ranking signals, PageRank, dofollow links, or submission volume.

## Load required controls

1. Read the approved project/product facts, brand rules, contact aliases, asset references, source list, authorization matrix, and existing record.
2. Read [references/seo-quality-gate.md](references/seo-quality-gate.md) before selecting or qualifying any site.
3. Read [references/authorization.md](references/authorization.md) before any action beyond read-only inspection.
4. Read [references/workflow.md](references/workflow.md) before browser work.
5. Read [references/browser-control-routing.md](references/browser-control-routing.md) before any browser or app interaction. Run the Windows/macOS/Linux capability preflight and select the backend from the current environment; do not assume a specific browser, operating system, or Computer Use support.
6. Read [references/status-model.md](references/status-model.md) before creating, updating, or auditing records.
7. Read [references/route-boundaries.md](references/route-boundaries.md) when a candidate is an article, community, email, contact, resource-page, or partnership route.
8. Copy [assets/submission-record-template.md](assets/submission-record-template.md) when no record exists.

Never invent company, developer, founder, pricing, address, launch, user-count, social, legal, ownership, affiliation, or contact facts. Leave optional unknowns blank; mark required unknowns `blocked — missing verified data`.

## Browser-first execution rule

For an ordinary website submission form, the default execution backend is a supported real browser runtime, connected browser extension, or desktop browser-control surface. Prefer structured DOM/form interaction from that runtime.

Use a direct API, CLI, or connector only when the target service exposes a documented or clearly supported programmatic submission interface and the required authorization is available.

Do **not** create or run ad-hoc per-site HTML parsers, guessed `requests`/`urllib` POSTs, hidden-field scrapers, or GitHub Actions that imitate browser form submissions. Browser routes can depend on JavaScript rendering, cookies, CSRF/session state, anti-bot systems, challenges, and UI-only terms. If no safe browser/API backend is available, preserve the record and hand off the blocked step to the user.

## Enforce the SEO purpose boundary

Stop the campaign if site selection, scale, anchor text, payment, reciprocal links, or automation is primarily intended to manipulate search rankings. Never promise rankings, PageRank, backlink counts, dofollow placement, domain-metric gains, or a “safe” submission volume.

Use only brand, project/product, site-name, or naked-URL anchors. Do not request dofollow treatment or use repeated commercial exact-match anchors. Record the actual public anchor, href, `rel`, and commercial or reciprocal relationship after publication. Require `sponsored` or `nofollow` treatment for paid or incentivized links; otherwise mark the placement noncompliant and do not count it as an acceptable listing.

## Restrict routes

Process only directory listings, request/recommendation forms, claims of existing directory listings, and project-bearing profiles on governed discovery platforms.

Do not batch articles, guest posts, community posts, press releases, cold email, contact-form promotion, or resource-page outreach through this workflow. Classify and hand them to a separate, route-specific workflow.

## Run Pass A — research, quality, and verification

1. Normalize source URLs and derive an idempotency key from platform domain, canonical project/product ID, account alias, and route.
2. Keep V2 in pilot mode: no more than 10 source sites per batch, with a separate opaque approval reference for every site when the strict authorization model is used.
3. Initialize each site with `Phase: eligibility`, `Status: not attempted`, and `Quality gate: not checked`.
4. Inspect relevance, real user/discovery value, governance/editorial oversight, link-selling claims, directory/network quality, reciprocal requirements, and automation/terms compatibility.
5. Mark low-quality, ranking-link, forced-reciprocal, irrelevant, empty-template, or directory-network candidates `ineligible` with structured evidence.
6. Allow form work only when every mandatory quality dimension passes and `Quality gate: passed`.
7. Reuse or create accounts only under a valid, scoped authorization entry.
8. Expose the earliest native verification, preserve interactive challenges, and build one manual queue. Never bypass or outsource a safeguard.
9. Enter no listing fields during Pass A. Read-only inspection and separately authorized registration are allowed.

## Run Pass B — authorized form execution

1. Recheck quality, duplicate state, verification validity, authorization validity, and source-list membership.
2. Start form work only on sites with `Quality gate: passed`.
3. Route normal website forms through the selected browser surface; use an official API only when documented and authorized.
4. Append an immutable event before or immediately after every executed action. Include timestamp, event ID, canonical action, result, and evidence-store reference.
5. Match every executed action to an `allowed` authorization whose approver, approval time, site scope, and expiry are valid at action time. Treat `ask` and `prohibited` as not authorized.
6. Fill only approved facts. Keep optional subscriptions off. Stop on missing required facts.
7. Submit only under valid final-submission authorization. Capture the exact visible/browser or official API response and structured evidence immediately.
8. Never retry an ambiguous final action. For `submission outcome unknown`, complete backend, mailbox, and public-page checks before any later attempt.

## Protect records and evidence

- Keep the public campaign record separate from the controlled evidence store.
- Record aliases and opaque evidence IDs, not passwords, OTPs, recovery codes, OAuth parameters, cookies, real session IDs, magic links, raw email addresses, phone numbers, or private absolute paths.
- Strip authentication and tracking parameters from record URLs. Preserve required route parameters only in the controlled evidence store.
- Set evidence capture and retention dates. Delete controlled evidence according to the campaign retention policy.
- Treat account creation, a click, navigation, a cleared form, or a saved draft as insufficient proof of submission.

## Close and audit

Run:

On macOS or Linux:

```bash
python3 scripts/audit_submission_record.py path/to/record.md
python3 scripts/audit_submission_record.py path/to/record.md --json
```

On Windows, use `py -3` or an equivalent Python 3 launcher:

```powershell
py -3 scripts/audit_submission_record.py path\to\record.md
py -3 scripts/audit_submission_record.py path\to\record.md --json
```

The auditor must fail on missing campaign controls, invalid or expired authorization, failed quality gates followed by execution, incompatible phase/status/evidence combinations, secret exposure, unsafe link relationships, duplicate idempotency keys, duplicate tracking variants, invalid event logs, or incomplete unknown-outcome checks.

Use qualified publication rate, referral visits, referral conversion, profile accuracy, and listing survival as KPIs. Do not use submission count, backlink count, dofollow count, DA, or DR as success criteria.

## Bundled resources

- [references/seo-quality-gate.md](references/seo-quality-gate.md): SEO purpose boundary and mandatory site-quality screening.
- [references/authorization.md](references/authorization.md): machine-auditable authorization model.
- [references/workflow.md](references/workflow.md): two-pass execution and recovery procedure.
- [references/browser-control-routing.md](references/browser-control-routing.md): backend-neutral browser selection, interaction, confirmation, recovery, and evidence rules.
- [references/status-model.md](references/status-model.md): state, evidence, event, and link-attribute rules.
- [references/route-boundaries.md](references/route-boundaries.md): supported routes and mandatory handoffs.
- [assets/submission-record-template.md](assets/submission-record-template.md): privacy-safe campaign template.
- `scripts/audit_submission_record.py`: deterministic record, authorization, quality, privacy, and idempotency auditor.
