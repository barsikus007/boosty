from time import time

from boosty.utils.client import ABCHTTPClient
from boosty.utils.json import dict_to_file, file_to_dict
from boosty.utils.logging import logger


class Auth:  # TODO vk auth
    access_token, refresh_token, expires_at, device_id, headers = None, None, None, None, None
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"  # noqa
    """https://techblog.willshouse.com/2012/01/03/most-common-user-agents/"""

    def __init__(
            self,
            auth_file: str = "auth.json",
            user_agent: str = DEFAULT_USER_AGENT,
    ):
        self.auth_file = auth_file
        self.user_agent = user_agent

        self.load_auth_data()

    def load_auth_data(self):
        try:
            auth_dict = file_to_dict(self.auth_file)
        except FileNotFoundError:
            logger.info(f"No auth file ({self.auth_file}) was found, using blank values (anonymous access mode)")
            auth_dict = {}
        self.access_token = auth_dict.get("access_token")
        self.refresh_token = auth_dict.get("refresh_token")
        self.expires_at = auth_dict.get("expires_at")
        self.device_id = auth_dict.get("device_id")
        self.headers = {"User-Agent": self.user_agent}
        if self.access_token:
            self.headers |= {"Authorization": f"Bearer {self.access_token}"}

    def save_auth_data(self):
        auth_data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "device_id": self.device_id,
        }
        dict_to_file(auth_data, self.auth_file)

    def save_auth_data_dotenv(self, dotenv_file=None):
        import dotenv  # noqa

        if not dotenv_file:
            dotenv_file = dotenv.find_dotenv()

        print(f".env file found: {dotenv_file}")
        dotenv.load_dotenv(dotenv_file)
        dotenv.set_key(dotenv_file, "ACCESS_TOKEN", self.access_token, "auto")
        dotenv.set_key(dotenv_file, "REFRESH_TOKEN", self.refresh_token, "auto")
        dotenv.set_key(dotenv_file, "EXPIRES_AT", self.expires_at, "auto")
        dotenv.set_key(dotenv_file, "DEVICE_ID", self.device_id, "auto")

    async def refresh_auth_data(self, session: ABCHTTPClient, api_url: str = ""):
        self.load_auth_data()
        if not self.refresh_token:
            raise ValueError("No refresh token was found to refresh auth data")

        response_data = await session.request_json(
            f"{api_url}/oauth/token/",
            method="POST",
            data={
                "device_id": self.device_id,
                "device_os": "web",
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
            headers=self.headers)

        try:
            self.refresh_token = response_data["refresh_token"]
            self.access_token = response_data["access_token"]
            self.expires_at = int(time()) + response_data["expires_in"]
        except KeyError as e:
            raise ValueError(f"Failed to refresh auth data: {response_data}") from e

        self.save_auth_data()
        self.load_auth_data()
