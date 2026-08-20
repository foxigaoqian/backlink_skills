---
name: backlink-submitter
description: Browser-first backlink discovery, qualification, submission, and lifecycle tracking for project websites such as game guides, tools, SaaS products, content sites, and independent web projects. Start from a project URL, infer the site type, select relevant free or approved channels, use a real browser or documented API to submit, hand off CAPTCHA/login/email verification to the user, and keep auditable campaign state. Do not use for spam, ranking manipulation, invented identities, CAPTCHA bypass, paid-link schemes, or forced reciprocal links.
---

# Backlink Submitter

Turn one project URL into a resumable, quality-first backlink campaign.

This skill is the default entry point for this fork. The user should be able to provide only a website URL and a short instruction such as:

```text
$backlink-submitter
给 https://example.com 做外链
```

The agent should research the site, infer safe defaults, build the campaign profile, select a small first batch, execute eligible submissions through the best available browser/API surface, and record every result truthfully.

## Core rule: browser first, API when official

For ordinary public submission forms, use a supported real browser runtime, connected browser extension, or desktop browser-control surface. Prefer structured DOM/form interaction exposed by that runtime.

Use a direct API/CLI adapter only when the target service documents an official or clearly supported programmatic submission interface and the required authorization is available.

Do **not** build or run ad-hoc per-site HTML scrapers, hidden-form parsers, guessed POST requests, or GitHub Actions that imitate browser form submissions. A page that works in a normal browser may return different HTML, JavaScript, cookies, anti-bot challenges, or session state to a headless HTTP client. Treat browser-visible UI as the source of truth for browser routes.

If no safe browser/API backend is available, stop at `ready — browser execution needed` instead of pretending the submission was automated.

## Load order

1. Read the target website and determine its public identity, site type, topic, market, and ownership/affiliation boundaries.
2. Read `../Free-backlink-list.md` as a candidate source, never as current truth.
3. Read `references/browser-first-routing.md` before any mutable external action.
4. For quality-first campaigns, reuse the quality principles from `../submit-product-directories-v2-quality/references/seo-quality-gate.md`.
5. For status/evidence semantics, reuse `../submit-product-directories-v2-quality/references/status-model.md` where compatible.
6. Create or update `../campaigns/<domain>.md` using `assets/campaign-template.md` when no record exists.

## Supported project types

Infer one primary type and optional secondary types:

- game guide / game wiki-style reference
- browser game / game portal
- SaaS / software / app
- AI tool
- developer / open-source project
- content / editorial site
- creator / portfolio project
- local business or other legitimate website

Do not force every site into SaaS/product directories. Channel selection must match the site's real identity.

## Channel families

Depending on the project type, consider:

- niche directories and discovery sites
- game/gaming directories for game projects
- software/app/SaaS directories for software projects
- developer/open-source showcases for developer projects
- general web directories only when they have real discovery value and acceptable quality
- contextual links from the user's own relevant public repositories or project documentation when editorially useful

Exclude or separate:

- irrelevant directories
- dead or inaccessible sites
- low-quality directory networks
- forced reciprocal links unless explicitly approved
- paid-only placements unless explicitly approved
- routes requiring the project to misrepresent itself as an official product, developer, company, or editable wiki
- article/community/contact-form outreach unless a separate route-specific workflow is requested

## Default campaign policy

Unless the user specifies otherwise:

- first batch: maximum 10 candidates
- payment: prohibited
- reciprocal link/site modification: prohibited
- exact-match commercial anchor campaigns: prohibited
- public anchor: brand/site name or naked canonical URL
- identity: truthful, including independent/fan/unofficial status where material
- newsletters/promotions: opt out when optional
- final submission: allowed for clearly free, relevant, ordinary directory forms when the user has asked to "submit backlinks" or equivalent
- CAPTCHA, Turnstile, email verification, OTP, login, account creation requiring user credentials, payment, or site modification: hand off to user unless a previously authorized session and runtime can safely complete the ordinary flow

## Workflow

### Phase 1 — project profile

From the live site and available project sources, establish:

- canonical URL
- public site name
- one-sentence truthful description
- longer description
- site type
- topic/category
- target market/language
- affiliation/ownership boundary
- preferred categories
- approved anchor variants
- allowed assets

Never invent company, developer, founder, pricing, address, release state, traffic, user counts, social accounts, or ownership facts.

### Phase 2 — candidate discovery and quality gate

1. Search the free backlink list for matching categories and historical notes.
2. Add new candidates found through current research when useful.
3. Revisit each candidate live before execution; old notes are not current facts.
4. Score practical fit using relevance, real discovery value, site quality/governance, current availability, cost, reciprocal requirement, verification burden, and expected listing durability.
5. Select no more than 10 candidates for the first batch.
6. Record exclusions with reasons rather than silently dropping them.

### Phase 3 — execution-surface routing

For each candidate, choose exactly one route:

1. **Official API/CLI/connector** — use when documented and authorized.
2. **Browser runtime / connected browser extension** — default for normal websites.
3. **Desktop browser control** — use when the active browser session must be preserved and supported.
4. **User handoff** — use for CAPTCHA, unavailable authentication, email confirmation, payment, or unsupported UI.

Do not substitute a guessed HTTP POST for a browser route.

### Phase 4 — browser submission

For browser-routed sites:

1. Open the current submission page.
2. Recheck cost, reciprocal requirement, category fit, login state, and visible terms.
3. Fill only approved profile data.
4. Prefer the most specific truthful category.
5. Keep optional promotions/newsletters off unless approved.
6. Before the final submit action, verify the target URL, public identity, selected category, cost, and agreements.
7. Submit once.
8. Capture the exact visible result and resulting URL.
9. Never infer success from a cleared form, disabled button, generic redirect, or transport success alone.
10. If the result is ambiguous, mark `submission outcome unknown` and do not retry until checked.

### Phase 5 — verification handoff

When a site presents CAPTCHA, Turnstile, image challenge, email verification, OTP, login requiring user credentials, or a security warning:

- preserve the current browser/session when possible;
- mark the record with the exact blocking step;
- ask the user to complete only that step;
- after handoff, re-read the page/session state before continuing;
- never bypass or outsource the safeguard.

### Phase 6 — lifecycle tracking

Use these practical states:

- `not attempted`
- `ready — browser execution needed`
- `blocked — user action`
- `blocked — email verification`
- `submitted`
- `awaiting approval`
- `published`
- `submission outcome unknown`
- `submission failed`
- `unavailable`
- `paid-only`
- `excluded`

For `published`, save the public listing URL and, when practical, the visible anchor/href/rel. Keep submitted and published separate.

## Campaign record

Every project should have one resumable record at:

```text
campaigns/<domain>.md
```

Update the record immediately after each meaningful result so another session can resume without duplicate submissions.

Do not put passwords, OTPs, cookies, recovery codes, session IDs, magic links, raw authentication URLs, or other secrets in the campaign record.

## Completion report

At the end of a batch, report only verified counts:

- candidates researched
- excluded / unavailable / paid-only
- ready for browser execution
- blocked for user action
- submitted
- awaiting approval
- published
- unknown outcome

Then list the next highest-priority actions. Do not claim SEO gains from submission volume alone.

## Handoff to V1/V2

- Use this skill as the normal entry point when the user starts from a project URL.
- Hand a large, already qualified URL list to `$submit-product-directories-v1-batch` when throughput and queue recovery are the main problem.
- Use `$submit-product-directories-v2-quality` when a campaign requires its stricter authorization matrix and formal quality audit.

The browser-first routing rule in this skill still applies: normal web forms belong in a browser runtime; official APIs may use programmatic adapters; ad-hoc HTTP form imitation is not a supported execution backend.
