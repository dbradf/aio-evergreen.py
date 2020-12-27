"""Evergreen representation of a project."""
from typing import List, Optional

from pydantic import BaseModel


class ProjectCommitQueue(BaseModel):
    """Status of commit queue for the project."""

    enabled: bool
    merge_method: str
    patch_type: str


class EvgProject(BaseModel):
    """Representation of an Evergreen project."""

    batch_time: int
    branch_name: str
    display_name: str
    enabled: bool
    identifier: str
    owner_name: str
    private: bool
    remote_path: str
    repo_name: str
    tracked: bool
    deactivated_previous: Optional[bool]
    admins: List[str]
    tracks_push_events: bool
    pr_testing_enabled: bool
    commit_queue: ProjectCommitQueue
