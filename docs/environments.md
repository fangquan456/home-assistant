# Development and production environments

Gendome has two strictly isolated runtime environments. The integration reads
`GENDOME_ENV` when Home Assistant starts. In this personal test repository, an
unset value defaults to `dev` so HACS custom-repository installs connect to the
development cloud. The official release repository must continue to default to
`prod`.

| Environment | API base URL | OAuth base URL | OAuth client | HA config | URL |
| --- | --- | --- | --- | --- | --- |
| dev | `https://dev-api.gendome.cloud` | `https://dev-oauth.gendome.cloud` | `gendome_home_assistant` | `config-dev` | `http://localhost:8123` |
| prod | `https://api.gendome.cloud` | `https://oauth.gendome.cloud` | `gendome_home_assistant` | `config-prod` | `http://localhost:8123` |

Never copy Application Credentials, `.storage`, tokens, or config entries
between these directories.

## Local development test

From the repository root:

```powershell
docker compose pull
docker compose up -d
docker compose ps
docker compose logs -f homeassistant
```

Complete Home Assistant onboarding at `http://localhost:8123`. Add Gendome and
confirm the flow redirects directly to
`https://dev-oauth.gendome.cloud/oauth/authorize`, includes an S256 PKCE
challenge, and does not ask for Application Credentials.

To exercise the legacy development fallback instead, set
`GENDOME_OAUTH_MODE=application_credentials`, restart Home Assistant, add the
dev Application Credential, and start a new Gendome config flow. Never enable
this mode in the normal HACS acceptance test.

Code changes are mounted read-only into the container. Restart Home Assistant
after a change:

```powershell
docker compose restart homeassistant
```

Stop or reset only the development environment:

```powershell
docker compose down
docker compose down -v
```

The bind-mounted `config-dev` directory remains after `down`. Delete it only
when an intentionally clean onboarding test is required.

## Production preflight

Production preflight is a separate Compose project, container, and HA
configuration, but it uses the same host port. Stop dev before starting prod:

```powershell
docker compose down
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml logs -f homeassistant
```

Open `http://localhost:8123`, use a safe production test account/device, and
confirm the built-in public PKCE client uses
`https://oauth.gendome.cloud/oauth/authorize` without a secret or an
implementation picker.

Stop production preflight without affecting dev:

```powershell
docker compose -f docker-compose.prod.yml down
```

## Test repository guard

Before HACS development testing, run without `GENDOME_ENV` or
`GENDOME_OAUTH_MODE` and verify the test-repository defaults:

```powershell
python -c "from custom_components.gendome.const import DEFAULT_API_BASE_URL, ENVIRONMENT, OAUTH_MODE; print(ENVIRONMENT, OAUTH_MODE, DEFAULT_API_BASE_URL)"
```

Expected output:

```text
dev public_pkce https://dev-api.gendome.cloud
```

Run Ruff, tests, compilation, dev acceptance, production preflight, and the
release checklist. GitHub/HACS does not use either Compose file, so this test
repository intentionally keeps the unset source-code default on development.
