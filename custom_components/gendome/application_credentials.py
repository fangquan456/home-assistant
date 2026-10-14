"""Gendome OAuth2 的应用凭据支持。"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, cast

from aiohttp import BasicAuth, ClientResponseError
from homeassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import (
    OAuth2TokenRequestError,
    OAuth2TokenRequestReauthError,
    OAuth2TokenRequestTransientError,
)
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    AUTHORIZE_URL,
    DEFAULT_API_BASE_URL,
    DEFAULT_OAUTH_BASE_URL,
    ENVIRONMENT,
    TOKEN_URL,
)


class GendomeOAuth2Implementation(AuthImplementation):
    """使用 Gendome 现有 Basic 客户端认证方式的 OAuth2 实现。"""

    async def _token_request(self, data: dict[str, Any]) -> dict[str, Any]:
        """使用 HTTP Basic 客户端认证方式请求 Token。"""
        request_data = dict(data)
        request_data.pop("client_id", None)
        request_data.pop("client_secret", None)

        session = async_get_clientsession(self.hass)
        try:
            response = await session.post(
                self.token_url,
                data=request_data,
                auth=BasicAuth(self.client_id, self.client_secret),
            )
            response.raise_for_status()
        except ClientResponseError as err:
            error_args = {
                "request_info": err.request_info,
                "history": err.history,
                "status": err.status,
                "message": err.message,
                "headers": err.headers,
                "domain": self.domain,
            }
            if err.status == HTTPStatus.TOO_MANY_REQUESTS or 500 <= err.status <= 599:
                raise OAuth2TokenRequestTransientError(**error_args) from err
            if 400 <= err.status <= 499:
                raise OAuth2TokenRequestReauthError(**error_args) from err
            raise OAuth2TokenRequestError(**error_args) from err

        return cast(dict[str, Any], await response.json())


async def async_get_authorization_server(
    hass: HomeAssistant,
) -> AuthorizationServer:
    """返回 Gendome OAuth2 授权服务配置。"""
    return AuthorizationServer(authorize_url=AUTHORIZE_URL, token_url=TOKEN_URL)


async def async_get_auth_implementation(
    hass: HomeAssistant,
    auth_domain: str,
    credential: ClientCredential,
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """返回兼容 Gendome 客户端认证方式的 OAuth2 实现。"""
    return GendomeOAuth2Implementation(
        hass,
        auth_domain,
        credential,
        await async_get_authorization_server(hass),
    )


async def async_get_description_placeholders(
    hass: HomeAssistant,
) -> dict[str, str]:
    """返回应用凭据弹窗使用的占位参数。"""
    return {
        "account_url": "https://www.gendome.com",
        "api_base_url": DEFAULT_API_BASE_URL,
        "oauth_base_url": DEFAULT_OAUTH_BASE_URL,
        "environment": ENVIRONMENT.upper(),
    }
