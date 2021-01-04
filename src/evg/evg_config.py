"""Get configuration about connecting to evergreen."""
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic.main import BaseModel

DEFAULT_NETWORK_TIMEOUT_SEC = timedelta(minutes=5).total_seconds()
DEFAULT_API_SERVER = "https://evergreen.mongodb.com"
CONFIG_FILE_LOCATIONS = [
    Path.home() / "cli_bin" / ".evergreen.yml",
    Path.home() / ".evergreen.yml",
]


class EvgConfigFile(BaseModel):
    """
    Contents of Evergreen Configuration file.

    user: Username to authenticate with.
    api_key: API Key of user.
    api_server_host: API server to connect to.
    """

    user: str
    api_key: str
    api_server_host: Optional[str]

    @classmethod
    def from_file(cls, path: Path) -> "EvgConfigFile":
        """
        Read evergreen config from given filename.

        :param path: Filename to read config.
        :return: Config read from file.
        """
        with open(path, "r") as fstream:
            return cls(**yaml.safe_load(fstream))


@dataclass
class EvgConfig:
    """
    Configuration to connect to evergreen api.

    api_server: Evergreen API server host.
    api_key: API Key of user to authenticate with.
    username: Username of user to authenticate with.
    network_timeout: Timeout to use for network calls.
    """

    api_server: str
    api_key: str
    username: str
    network_timeout: int

    @classmethod
    def from_file(
        cls, path: Path, network_timeout: int = DEFAULT_NETWORK_TIMEOUT_SEC
    ) -> "EvgConfig":
        """
        Read evergreen config from given filename.

        :param path: Filename to read config.
        :param network_timeout: Timeout to use for network calls.
        :return: Config read from file.
        """
        config_file_contents = EvgConfigFile.from_file(path)
        api_server = DEFAULT_API_SERVER
        if config_file_contents.api_server_host:
            api_server = config_file_contents.api_server_host
        return cls(
            api_key=config_file_contents.api_key,
            username=config_file_contents.user,
            api_server=api_server,
            network_timeout=network_timeout,
        )

    @classmethod
    def find_default_config(
        cls, network_timeout: int = DEFAULT_NETWORK_TIMEOUT_SEC
    ) -> Optional["EvgConfig"]:
        """
        Search known location for the evergreen config file.

        :return: First found evergreen configuration.
        """
        for filename in [filename for filename in CONFIG_FILE_LOCATIONS if filename.exists()]:
            return cls.from_file(filename, network_timeout=network_timeout)

        return None

    def get_auth_headers(self) -> Dict[str, str]:
        """Get HTTP headers to authenticate. """
        return {"Api-User": self.username, "Api-Key": self.api_key}
