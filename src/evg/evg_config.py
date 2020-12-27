"""Get configuration about connecting to evergreen."""
from datetime import timedelta
from pathlib import Path
from typing import Dict, NamedTuple, Optional

import yaml
from pydantic.main import BaseModel

DEFAULT_NETWORK_TIMEOUT_SEC = timedelta(minutes=5).total_seconds()
DEFAULT_API_SERVER = "https://evergreen.mongodb.com"
CONFIG_FILE_LOCATIONS = [
    Path.home() / "cli_bin" / ".evergreen.yml",
    Path.home() / ".evergreen.yml",
]


class EvgAuth(NamedTuple):

    username: str
    api_key: str

    def get_auth_headers(self) -> Dict[str, str]:
        return {"Api-User": self.username, "Api-Key": self.api_key}


class EvgConfig(BaseModel):

    user: str
    api_key: str
    api_server_host: str
    ui_server_host: str

    @classmethod
    def from_file(cls, path: Path) -> "EvgConfig":
        """
        Read evergreen config from given filename.

        :param path: Filename to read config.
        :return: Config read from file.
        """
        with open(path, "r") as fstream:
            return cls(**yaml.safe_load(fstream))

    @classmethod
    def find_default_config(cls) -> Optional["EvgConfig"]:
        """
        Search known location for the evergreen config file.

        :return: First found evergreen configuration.
        """
        for filename in [filename for filename in CONFIG_FILE_LOCATIONS if filename.exists()]:
            return EvgConfig.from_file(filename)

        return None

    def get_auth(self) -> EvgAuth:
        return EvgAuth(username=self.user, api_key=self.api_key)
