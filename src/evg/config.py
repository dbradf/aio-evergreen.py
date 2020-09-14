"""Configuration for evergreen client."""
import os
from typing import Dict, NamedTuple, Optional

import yaml

DEFAULT_CONFIG_FILE = os.path.expanduser(os.path.join("~", ".evergreen.yml"))

class EvgAuth(NamedTuple):

    username: Optional[str]
    api_key: Optional[str]

    def auth_headers(self) -> Dict[str, str]:
        headers = {}
        if self.username:
            headers["Auth-User"] = self.username
        if self.api_key:
            headers["Auth-Api"] = self.api_key

        return headers

    @classmethod
    def from_file(cls, filename: str = DEFAULT_CONFIG_FILE) -> "EvgAuth":
        config = read_evergreen_from_file(filename)
        return cls(username=config.get("user"), api_key=config.get("api_key"))


def read_evergreen_from_file(filename: str):
    with open(filename) as fstream:
        return yaml.safe_load(fstream)