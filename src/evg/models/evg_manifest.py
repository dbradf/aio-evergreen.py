"""Representation of evergreen manifest."""
from typing import Dict

from pydantic.main import BaseModel


class EvgManifestModule(BaseModel):
    """Represents a module in the evergreen manifest."""

    branch: str
    repo: str
    revision: str
    owner: str
    url: str


class EvgManifest(BaseModel):
    """Representation of an evergreen manifest."""

    id: str
    revision: str
    project: str
    branch: str
    modules: Dict[str, EvgManifestModule]
