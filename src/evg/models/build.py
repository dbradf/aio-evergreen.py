"""Models for evergreen build results."""
from datetime import datetime
from typing import List

from pydantic import BaseModel


class StatusCounts(BaseModel):
    """Status counts of an evergreen build."""

    succeeded: int
    failed: int
    undispatched: int
    inactive: int
    dispatched: int
    timed_out: int


class EvgBuild(BaseModel):
    """Model of an evergreen build."""

    id: str
    project_id: str
    create_time: datetime
    start_time: datetime
    finish_time: datetime
    version: str
    branch: str
    git_hash: str
    build_variant: str
    status: str
    activated: bool
    activated_by: str
    order: int
    time_taken_ms: int
    display_name: str
    predicted_makespace_ms: int
    actual_makespan_ms: int
    origin: str
    status_counts: StatusCounts
    tasks: List[str]

    def __repr__(self) -> str:
        """Get a string representation."""
        return f"EvgBuild({self.id})"
