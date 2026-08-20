# Browser-first execution routing

Use the execution surface that matches the route the website actually exposes.

## Decision order

1. If the service documents an official API, CLI, connector, or other supported programmatic submission method and authorization is available, use it.
2. Otherwise, for an ordinary website form, use a supported real browser runtime or connected browser extension.
3. If the form requires the user's existing authenticated browser session and the runtime supports desktop browser control, preserve that session.
4. If CAPTCHA, Turnstile, OTP, email verification, unavailable login, payment, or unsupported UI blocks execution, hand the step to the user.

## Explicitly unsupported shortcut

Do not convert a browser route into an ad-hoc HTTP automation route merely because the HTML appears simple.

Avoid:

- guessed `requests`/`urllib` POSTs to normal website forms
- hidden-field scraping used to imitate an interactive browser
- one Python adapter per directory when there is no documented API
- GitHub Actions that submit third-party website forms by pretending to be a browser
- retry loops after ambiguous final submissions

Why: browser routes can depend on client-side rendering, cookies, CSRF/session state, bot protection, JavaScript, challenge state, or UI-only terms. The response received by a generic HTTP client can differ from what a real user sees.

## Browser interaction rules

- Prefer structured DOM/form controls exposed by the active runtime.
- Re-read page state after navigation, modal changes, login, CAPTCHA handoff, or submission.
- Fill only verified project data.
- Recheck category, cost, reciprocal requirements, agreements, and target URL before submitting.
- Submit once.
- Record the exact visible response and resulting URL.
- A successful click or HTTP navigation is not submission evidence by itself.

## User handoff

Handoff is a normal state, not a failure. Preserve the work and state exactly what the user needs to do, for example:

- solve the visible CAPTCHA
- confirm an email
- sign in to an existing account
- approve a paid plan (only if campaign policy permits)

After the user completes the step, reacquire current page state instead of reusing stale selectors or assuming the challenge is still valid.

## Evidence

Record:

- route type: official API / browser / desktop browser / user handoff
- timestamp
- submission page
- result text or server response
- resulting URL
- public listing URL when published
- next action

Never store passwords, cookies, OTPs, recovery codes, session IDs, or authentication URLs in shareable records.
