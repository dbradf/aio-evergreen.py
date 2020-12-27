"""Representation of an evergreen build."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

EVG_BUILD_STATUS_FAILED = "failed"
EVG_BUILD_STATUS_SUCCESS = "success"
EVG_BUILD_STATUS_CREATED = "created"

COMPLETED_STATES = {
    EVG_BUILD_STATUS_FAILED,
    EVG_BUILD_STATUS_SUCCESS,
}


class StatusCounts(BaseModel):
    """Representation of Evergreen StatusCounts."""

    succeeded: int
    failed: int
    started: int
    undispatched: int
    inactivate: Optional[int]
    dispatched: int
    timed_out: int


class EvgBuild(BaseModel):
    """Representation of an Evergreen build."""

    id: str = Field(alias="_id")
    project_id: str
    create_time: Optional[datetime]
    start_time: Optional[datetime]
    finish_time: Optional[datetime]
    version: str
    branch: str
    git_hash: str
    build_variant: str
    status: str
    activated: bool
    activated_by: str
    activated_time: Optional[datetime]
    order: int
    tasks: List[str]
    time_taken_ms: int
    display_name: str
    predicted_makespan_ms: int
    actual_makespan_ms: int
    origin: str
    status_counts: StatusCounts

    def is_completed(self) -> bool:
        """
        Determine if this build has completed running tasks.

        :return: True if build has completed running tasks.
        """
        return self.status in COMPLETED_STATES
