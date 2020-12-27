"""Version representation of evergreen."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, PrivateAttr


class Requester(Enum):
    """Requester that created version."""

    PATCH_REQUEST = "patch_request"
    GITTER_REQUEST = "gitter_request"
    GITHUB_PULL_REQUEST = "github_pull_request"
    MERGE_TEST = "merge_test"
    AD_HOC = "ad_hoc"
    TRIGGER_REQUEST = "trigger_request"
    UNKNOWN = "unknown"

    def evg_value(self) -> str:
        """Get the evergreen value for a requester."""
        return self.name.lower()

    def stats_value(self) -> str:
        """Get the value for the stats endpoints."""
        value_mappings = {
            Requester.PATCH_REQUEST: "patch",
            Requester.GITTER_REQUEST: "mainline",
            Requester.GITHUB_PULL_REQUEST: "patch",
            Requester.MERGE_TEST: "",
            Requester.AD_HOC: "adhoc",
            Requester.TRIGGER_REQUEST: "trigger",
            Requester.UNKNOWN: "",
        }

        return value_mappings[self]


PATCH_REQUESTERS = {
    Requester.PATCH_REQUEST,
    Requester.GITHUB_PULL_REQUEST,
    Requester.MERGE_TEST,
}

EVG_VERSION_STATUS_SUCCESS = "success"
EVG_VERSION_STATUS_FAILED = "failed"
EVG_VERSION_STATUS_CREATED = "created"

COMPLETED_STATES = {
    EVG_VERSION_STATUS_FAILED,
    EVG_VERSION_STATUS_SUCCESS,
}


class BuildVariantStatus(BaseModel):
    """Representation of a Build Variants status."""

    build_variant: str
    build_id: str


class EvgVersion(BaseModel):
    """Representation of an Evergreen Version."""

    version_id: str
    create_time: datetime
    start_time: Optional[datetime]
    finish_time: Optional[datetime]
    revision: str
    order: int
    project: str
    author: str
    author_email: str
    message: str
    status: str
    repo: str
    branch: str
    errors: List[str]
    ignored = bool
    requester: Optional[Requester]
    build_variants_status: Optional[List[BuildVariantStatus]]

    _build_variants_map: Dict[str, str] = PrivateAttr()

    def __init__(self, **json: Dict[str, Any]) -> None:
        """
        Create an instance of an evergreen version.

        :param json: json representing version
        """
        super().__init__(**json)

        self._build_variants_map = {}

        if self.build_variants_status:
            self._build_variants_map = {
                bvs.build_variant: bvs.build_id for bvs in self.build_variants_status
            }

    def is_patch(self) -> bool:
        """
        Determine if this version from a patch build.

        :return: True if this version is a patch build.
        """
        if self.requester and self.requester != Requester.UNKNOWN:
            return self.requester in PATCH_REQUESTERS
        return not self.version_id.startswith(self.project.replace("-", "_"))

    def is_completed(self) -> bool:
        """
        Determine if this version has completed running tasks.

        :return: True if version has completed.
        """
        return self.status in COMPLETED_STATES

    def __repr__(self) -> str:
        """
        Get the string representation of Version for debugging purposes.

        :return: String representation of Version.
        """
        return "Version({id})".format(id=self.version_id)
