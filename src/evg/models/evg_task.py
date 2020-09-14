"""Models for representing Evergreen tasks."""
from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class Artifact(BaseModel):
    """Model of an artifact attached to a task."""

    name: str
    url: str
    visibility: str
    ignore_for_fetch: bool


class StatusDetails(BaseModel):
    """Model of the details about task status."""

    status: str
    type: str
    desc: str
    timed_out: bool


class EvgTask(BaseModel):
    """Model for an evergreen task."""

    activated: bool
    activated_by: str
    artifacts: List[Artifact]
    build_id: str
    build_variant: str
    create_time: datetime
    depends_on: List[str]
    dispatch_time: datetime
    display_name: str
    display_only: bool
    distro_id: str
    est_wait_to_start_ms: int
    estimated_cost: float
    execution: int
    execution_tasks: str
    expected_duration_ms: int
    finish_time: datetime
    generate_task: bool
    generated_by: str
    host_id: str
    ingest_time: datetime
    logs: Dict[str, str]
    mainline: bool
    order: int
    project_id: str
    priority: int
    restarts: int
    revision: str
    scheduled_time: datetime
    start_time: datetime
    status: str
    status_details: StatusDetails
    task_group: str
    task_group_max_hosts: int
    task_id: str
    time_take_ms: int
    version_id: str

    def __repr__(self) -> str:
        """Get string representation of a task."""
        return f"EvgTask({self.task_id})"
