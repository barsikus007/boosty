from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import time


@dataclass
class AuthData:
    access_token: str | None = None
    refresh_token: str | None = None
    expires_at: str | None = None
    device_id: str | None = None
    user_agent: str | None = None

    @property
    def anonymous(self) -> bool:
        return self.access_token is None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "device_id": self.device_id,
            "user_agent": self.user_agent,
        }

    def from_response_data(self, response_data):
        try:
            self.refresh_token = response_data["refresh_token"]
            self.access_token = response_data["access_token"]
            self.expires_at = int(time()) + response_data["expires_in"]
        except KeyError as e:
            msg = f"Failed to refresh auth data: {response_data}"
            raise ValueError(msg) from e

    def from_cookies_data(self, response_data):
        try:
            self.refresh_token = response_data["refreshToken"]
            self.access_token = response_data["accessToken"]
            self.expires_at = response_data["expiresAt"]
        except KeyError as e:
            msg = f"Failed to refresh auth data: {response_data}"
            raise ValueError(msg) from e


class ABCAuthDataResolver(ABC):
    auth_data: AuthData

    @abstractmethod
    def load_auth_data(self) -> AuthData:
        pass

    @abstractmethod
    def save_auth_data(self):
        pass
