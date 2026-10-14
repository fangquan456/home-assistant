"""Tests for strict development and production environment isolation."""

import pytest

from custom_components.gendome.const import (
    ENVIRONMENT_DEV,
    ENVIRONMENT_PROD,
    OAUTH_MODE_APPLICATION_CREDENTIALS,
    OAUTH_MODE_PUBLIC_PKCE,
    OAUTH_SCOPE,
    OAUTH_SCOPES,
    REVOKE_URL,
    environment_api_base_url,
    environment_oauth_base_url,
    resolve_environment,
    resolve_oauth_mode,
)


def test_unset_environment_defaults_to_development(monkeypatch) -> None:
    monkeypatch.delenv("GENDOME_ENV", raising=False)

    assert resolve_environment() == ENVIRONMENT_DEV


def test_development_uses_development_api() -> None:
    assert (
        environment_api_base_url(ENVIRONMENT_DEV)
        == "https://dev-api.gendome.cloud"
    )


def test_production_uses_shared_overseas_api() -> None:
    assert (
        environment_api_base_url(ENVIRONMENT_PROD)
        == "https://api.gendome.cloud"
    )


def test_development_uses_development_oauth_server() -> None:
    assert (
        environment_oauth_base_url(ENVIRONMENT_DEV)
        == "https://dev-oauth.gendome.cloud"
    )


def test_production_uses_production_oauth_server() -> None:
    assert (
        environment_oauth_base_url(ENVIRONMENT_PROD)
        == "https://oauth.gendome.cloud"
    )


def test_unknown_environment_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="Unsupported GENDOME_ENV"):
        resolve_environment("staging")


def test_unset_oauth_mode_defaults_to_public_pkce(monkeypatch) -> None:
    monkeypatch.delenv("GENDOME_OAUTH_MODE", raising=False)

    assert resolve_oauth_mode() == OAUTH_MODE_PUBLIC_PKCE


def test_application_credentials_mode_must_be_explicit() -> None:
    assert (
        resolve_oauth_mode("application_credentials")
        == OAUTH_MODE_APPLICATION_CREDENTIALS
    )


def test_unknown_oauth_mode_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="Unsupported GENDOME_OAUTH_MODE"):
        resolve_oauth_mode("client_secret")


def test_oauth_scope_contains_only_supported_v1_permissions() -> None:
    assert " ".join(OAUTH_SCOPES) == OAUTH_SCOPE
    assert set(OAUTH_SCOPES) == {
        "device:read",
        "statistics:read",
        "device:control:switch",
        "device:control:setting",
        "scheduled_charging:read",
        "scheduled_charging:write",
    }


def test_revoke_endpoint_uses_current_oauth_environment() -> None:
    assert REVOKE_URL.endswith("/oauth/revokeToken")
