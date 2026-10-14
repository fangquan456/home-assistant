# Changelog

## Unreleased

- Added the built-in public OAuth client with Authorization Code + S256 PKCE.
- Normal HACS setup now opens the Gendome browser login directly, without an
  implementation picker or user-managed Application Credentials.
- Kept Application Credentials as an explicit development-only fallback via
  `GENDOME_OAUTH_MODE=application_credentials`.
- Added OAuth authorization revocation when a Gendome config entry is removed.
- Documented the Gendome browser login, consent, callback, revocation,
  production configuration, and rollout contract. App deep links remain an
  optional future enhancement.

## 1.0.0 - 2026-07-15

- Added standard OAuth2 account linking with Home Assistant Application
  Credentials and reauthentication.
- Added Gendome Home 3000 and Go series device discovery.
- Added coordinated battery, power, connectivity, charging, and firmware state
  entities.
- Added AC input, AC output, DC output, charge-power, battery-protection, and
  scheduled-charging controls.
- Added command idempotency keys, final-result polling, refresh button, regional
  API routing, error mapping, and privacy-safe diagnostics.
- Added HACS metadata, Docker development environment, CI validation, tests,
  installation documentation, troubleshooting, and release checklist.
