"""Gendome 集成常量。"""

from __future__ import annotations

import os
from datetime import timedelta
from typing import Final

DOMAIN: Final = "gendome"
NAME: Final = "Gendome"
MANUFACTURER: Final = "Gendome"

PRODUCT_KEY_GO_1000: Final = "woibp7yhn3w9qqr2"
PRODUCT_KEY_GO_2000: Final = "qvwckuhm3ykiomiz"
BEIYITONG_PRODUCT_KEYS: Final = frozenset(
    {PRODUCT_KEY_GO_1000, PRODUCT_KEY_GO_2000}
)

PLATFORMS: Final = (
    "sensor",
    "binary_sensor",
    "switch",
    "number",
    "button",
)

ENVIRONMENT_VARIABLE: Final = "GENDOME_ENV"
ENVIRONMENT_DEV: Final = "dev"
ENVIRONMENT_PROD: Final = "prod"
SUPPORTED_ENVIRONMENTS: Final = frozenset({ENVIRONMENT_DEV, ENVIRONMENT_PROD})
DEFAULT_ENVIRONMENT: Final = ENVIRONMENT_DEV

OAUTH_MODE_VARIABLE: Final = "GENDOME_OAUTH_MODE"
OAUTH_MODE_PUBLIC_PKCE: Final = "public_pkce"
OAUTH_MODE_APPLICATION_CREDENTIALS: Final = "application_credentials"
SUPPORTED_OAUTH_MODES: Final = frozenset(
    {OAUTH_MODE_PUBLIC_PKCE, OAUTH_MODE_APPLICATION_CREDENTIALS}
)

ENVIRONMENT_API_BASE_URLS: Final = {
    ENVIRONMENT_DEV: "https://dev-api.gendome.cloud",
    ENVIRONMENT_PROD: "https://api.gendome.cloud",
}

ENVIRONMENT_OAUTH_BASE_URLS: Final = {
    ENVIRONMENT_DEV: "https://dev-oauth.gendome.cloud",
    ENVIRONMENT_PROD: "https://oauth.gendome.cloud",
}


def resolve_environment(value: str | None = None) -> str:
    """解析并校验运行环境。

    个人测试仓库默认使用开发环境，便于通过 HACS 验证 dev 云服务。
    """
    environment = (value or os.getenv(ENVIRONMENT_VARIABLE, DEFAULT_ENVIRONMENT))
    environment = environment.strip().lower()
    if environment not in SUPPORTED_ENVIRONMENTS:
        supported = ", ".join(sorted(SUPPORTED_ENVIRONMENTS))
        raise RuntimeError(
            f"Unsupported {ENVIRONMENT_VARIABLE}={environment!r}; "
            f"expected one of: {supported}"
        )
    return environment


def environment_api_base_url(environment: str) -> str:
    """返回指定环境唯一的 API 基础地址。"""
    normalized = resolve_environment(environment)
    return ENVIRONMENT_API_BASE_URLS[normalized]


def environment_oauth_base_url(environment: str) -> str:
    """返回指定环境的 OAuth 授权服务基础地址。"""
    normalized = resolve_environment(environment)
    return ENVIRONMENT_OAUTH_BASE_URLS[normalized]


def resolve_oauth_mode(value: str | None = None) -> str:
    """Resolve the OAuth implementation used by new config flows.

    HACS installations always default to the public PKCE client. Application
    Credentials remain available only when a developer explicitly opts in.
    """
    mode = value or os.getenv(OAUTH_MODE_VARIABLE, OAUTH_MODE_PUBLIC_PKCE)
    mode = mode.strip().lower()
    if mode not in SUPPORTED_OAUTH_MODES:
        supported = ", ".join(sorted(SUPPORTED_OAUTH_MODES))
        raise RuntimeError(
            f"Unsupported {OAUTH_MODE_VARIABLE}={mode!r}; "
            f"expected one of: {supported}"
        )
    return mode


ENVIRONMENT: Final = resolve_environment()
OAUTH_MODE: Final = resolve_oauth_mode()
DEFAULT_API_BASE_URL: Final = environment_api_base_url(ENVIRONMENT)
DEFAULT_OAUTH_BASE_URL: Final = environment_oauth_base_url(ENVIRONMENT)
AUTHORIZE_URL: Final = f"{DEFAULT_OAUTH_BASE_URL}/oauth/authorize"
TOKEN_URL: Final = f"{DEFAULT_OAUTH_BASE_URL}/oauth/token"
REVOKE_URL: Final = f"{DEFAULT_OAUTH_BASE_URL}/oauth/revokeToken"
OPENAPI_PREFIX: Final = "/aiot-devicecenter/openapi/home-assistant"

PUBLIC_OAUTH_CLIENT_ID: Final = "gendome_home_assistant"
PUBLIC_OAUTH_IMPLEMENTATION: Final = "gendome_public_pkce"

CONF_API_BASE_URL: Final = "api_base_url"
CONF_ENVIRONMENT: Final = "environment"
CONF_REGION: Final = "region"

OAUTH_SCOPES: Final = (
    "device:read",
    "statistics:read",
    "device:control:switch",
    "device:control:setting",
    "scheduled_charging:read",
    "scheduled_charging:write",
)
OAUTH_SCOPE: Final = " ".join(OAUTH_SCOPES)

DEFAULT_SCAN_INTERVAL: Final = timedelta(seconds=60)
REQUEST_TIMEOUT_SECONDS: Final = 15
COMMAND_TIMEOUT_SECONDS: Final = 30
COMMAND_POLL_INTERVAL_SECONDS: Final = 2

COMMAND_SET_AC_INPUT: Final = "SET_AC_INPUT_ENABLED"
COMMAND_SET_AC_OUTPUT: Final = "SET_AC_OUTPUT_ENABLED"
COMMAND_SET_DC_OUTPUT: Final = "SET_DC_OUTPUT_ENABLED"
COMMAND_SET_BUZZER: Final = "SET_BUZZER_ENABLED"
COMMAND_SET_AC_CHARGE_POWER: Final = "SET_AC_CHARGE_POWER"
COMMAND_SET_BATTERY_RANGE: Final = "SET_BATTERY_PROTECTION_RANGE"
COMMAND_REFRESH_STATE: Final = "REFRESH_STATE"

TERMINAL_COMMAND_STATUSES: Final = frozenset(
    {"SUCCESS", "FAILED", "TIMEOUT", "REJECTED"}
)
FAILED_COMMAND_STATUSES: Final = frozenset({"FAILED", "TIMEOUT", "REJECTED"})
