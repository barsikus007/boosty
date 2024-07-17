from pathlib import Path

from boosty.api.auth.resolvers.abc import ABCAuthDataResolver, AuthData
from boosty.utils.json import dict_to_file, file_to_dict
from boosty.utils.logging import logger
from boosty.utils.types import StrPath


class FileAuthDataResolver(ABCAuthDataResolver):
    def __init__(
        self,
        *,
        auth_file: StrPath = "auth.json",
    ):
        self.auth_file = Path(auth_file)

    def load_auth_data(self):
        try:
            auth_dict = file_to_dict(self.auth_file)
        except FileNotFoundError:
            logger.info(f"Auth file ({self.auth_file}) wasn't found, using blank values (anonymous access mode)")
            auth_dict = {}

        self.auth_data = AuthData(**auth_dict)
        return self.auth_data

    def save_auth_data(self):
        if self.auth_data.anonymous:
            return
        dict_to_file(self.auth_data.to_dict(), self.auth_file)
