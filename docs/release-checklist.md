# Release and acceptance checklist

## HACS browser OAuth, backend, and OAuth

- [ ] Register `gendome_home_assistant` as a public client in isolated dev and
  production databases, with no client secret and token authentication `none`.
- [ ] Require S256 PKCE on authorization-code requests and validate the verifier
  during code exchange.
- [ ] Verify normal HACS setup opens the Gendome website directly without an
  implementation picker or Application Credentials form.
- [ ] Verify browser login, allow, reject, token refresh, and revocation all
  return to or update the originating Home Assistant instance.
- [ ] Complete development testing with `GENDOME_ENV=dev` and `config-dev`.
- [ ] Complete production preflight with `GENDOME_ENV=prod` and `config-prod`.
- [ ] Confirm no secret exists for the production public client and no OAuth
  secret is embedded in the HACS package.
- [ ] Allow the exact `https://my.home-assistant.io/redirect/oauth` callback and
  verify the declared `my` dependency returns to Docker and HAOS instances.
- [ ] Verify authorization-code exchange, refresh, rotation, and revocation.
- [ ] Enforce scopes, device ownership, online state, capabilities, command
  allow-list, idempotency, cooldown, and rate limits.
- [ ] Persist authorization, access audit, and command records with the agreed
  token/email/IP/SN/MAC redaction policy.
- [ ] Confirm GLOBAL, US, and EU gateway routes.

## Device and entity acceptance

- [ ] Test Home 3000, Go 300, Go 800, an online device, an offline device, and a
  multi-device account.
- [ ] Confirm SOC, SOH, remaining-time unit, all input/output power values,
  charge/discharge rules, and firmware values against the Gendome App.
- [ ] Confirm the capability/data-point matrix, including buzzer support and AC
  charge power bounds per model.
- [ ] Verify stable unique IDs, correct device grouping, no duplicate entities,
  restart recovery, and offline availability.

## Control and failure acceptance

- [ ] Test AC input, AC output, DC output, charge power, lower/upper SOC,
  scheduled charging, and refresh state.
- [ ] Correlate HA action, command table, device receipt, App state, and final HA
  state for every command.
- [ ] Exercise 401, 403, 429, 500, network timeout, revoked refresh token,
  offline device, missing property, command timeout, and duplicate command.

## Distribution

- [ ] Verify this test-repository installation without `GENDOME_ENV` defaults
  to `https://dev-api.gendome.cloud`.
- [ ] Verify an installation without `GENDOME_OAUTH_MODE` defaults to
  `public_pkce`.
- [x] Confirm GitHub repository, documentation, and issue tracker values use
  `https://github.com/gendome/home-assistant`.
- [x] Set the public code owner to `@fangquan456`.
- [ ] Run tests, Ruff, JSON validation, Home Assistant Docker, and HAOS tests.
- [ ] Validate HACS custom-repository install and upgrade.
- [ ] Publish the release with release notes and complete a limited user rollout.
