from boosty.api.auth.resolvers.abc import ABCAuthDataResolver, AuthData
from boosty.api.auth.resolvers.file import FileAuthDataResolver
from boosty.utils.client import ABCHTTPClient
from boosty.utils.consts import DEFAULT_USER_AGENT


class Auth:
    def __init__(
        self,
        auth_resolver: ABCAuthDataResolver | None = None,
    ):
        self.auth_resolver = FileAuthDataResolver() if auth_resolver is None else auth_resolver

        self.auth_data: AuthData = self.auth_resolver.load_auth_data()

    @property
    def headers(self) -> dict[str, str]:
        if not self.auth_data.user_agent:
            self.auth_data.user_agent = DEFAULT_USER_AGENT
            self.auth_resolver.save_auth_data()
        headers = {"User-Agent": self.auth_data.user_agent}
        if self.auth_data.access_token:
            headers |= {"Authorization": f"Bearer {self.auth_data.access_token}"}
        return headers

    async def refresh_auth_data(self, session: ABCHTTPClient, api_url: str):
        self.auth_data = self.auth_resolver.load_auth_data()
        if not self.auth_data.refresh_token:
            raise ValueError("No refresh token was found to refresh auth data")

        response_data = await session.request_json(
            f"{api_url}/oauth/token/",
            method="POST",
            data={
                "device_id": self.auth_data.device_id,
                "device_os": "web",
                "grant_type": "refresh_token",
                "refresh_token": self.auth_data.refresh_token,
            },
            headers=self.headers,
        )

        self.auth_data.from_response_data(response_data)

        self.auth_resolver.save_auth_data()
        self.auth_resolver.load_auth_data()
