"""Task representation of evergreen."""
from datetime import datetime, timedelta
from enum import IntEnum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Extra

EVG_SUCCESS_STATUS = "success"
EVG_SYSTEM_FAILURE_STATUS = "system"
EVG_UNDISPATCHED_STATUS = "undispatched"

_EVG_DATE_FIELDS_IN_TASK = frozenset(
    ["create_time", "dispatch_time", "finish_time", "ingest_time", "scheduled_time", "start_time"]
)


class EvgArtifact(BaseModel):
    """Representation of a task artifact from evergreen."""

    name: str
    url: str
    visibility: str
    ignore_for_fetch: bool


class StatusScore(IntEnum):
    """Integer score of the task status."""

    SUCCESS = 1
    FAILURE = 2
    FAILURE_SYSTEM = 3
    FAILURE_TIMEOUT = 4
    UNDISPATCHED = 5

    @classmethod
    def get_task_status_score(cls, task: "EvgTask") -> "StatusScore":
        """
        Retrieve the status score based on the task status.

        :return: Status score.
        """
        if task.is_success():
            return StatusScore.SUCCESS
        if task.is_undispatched():
            return StatusScore.UNDISPATCHED
        if task.is_timeout():
            return StatusScore.FAILURE_TIMEOUT
        if task.is_system_failure():
            return StatusScore.FAILURE_SYSTEM
        return StatusScore.FAILURE


class StatusDetails(BaseModel):
    """Representation of a task status details from evergreen."""

    status: str
    type: str
    desc: str
    timed_out: bool


class DisplayTaskDependency(BaseModel):
    """Dependency on a display task."""

    id: str
    status: str


class EvgTask(BaseModel):
    """Representation of an Evergreen task."""

    activated: bool
    activated_by: str
    artifacts: Optional[List[EvgArtifact]]
    build_id: str
    build_variant: str
    create_time: datetime
    depends_on: Optional[List[Union[str, DisplayTaskDependency]]]
    dispatch_time: Optional[datetime]
    display_name: str
    display_only: bool
    distro_id: str
    est_wait_to_start_ms: int
    estimated_cost: float
    execution: int
    execution_tasks: Optional[List[str]]
    expected_duration_ms: int
    finish_time: Optional[datetime]
    generate_task: bool
    generated_by: str
    host_id: str
    ingest_time: Optional[datetime]
    logs: Dict[str, Optional[str]]
    mainline: Optional[bool]
    order: int
    project_id: str
    priority: int
    restarts: int
    revision: str
    scheduled_time: Optional[datetime]
    start_time: Optional[datetime]
    status: str
    status_details: StatusDetails
    task_group: Optional[str]
    task_group_max_hosts: Optional[int]
    task_id: str
    time_taken_ms: int
    version_id: str

    def get_status_score(self) -> StatusScore:
        """
        Retrieve the status score enum for the given task.

        :return: Status score.
        """
        return StatusScore.get_task_status_score(self)

    def get_execution(self, execution: int) -> Optional["EvgTask"]:
        """
        Get the task info for the specified execution.

        :param execution: Index of execution.
        :return: Task info for specified execution.
        """
        if self.execution == execution:
            return self

        raw_task = self.dict()
        for task in raw_task.get("previous_executions", []):
            if task.get("execution") == execution:
                return EvgTask(**task)

        return None

    def get_execution_or_self(self, execution: int) -> "EvgTask":
        """
        Get the specified execution if it exists.

        If the specified execution does not exist, return self.

        :param execution: Index of execution.
        :return: Task info for specified execution or self.
        """
        task_execution = self.get_execution(execution)
        if task_execution:
            return task_execution
        return self

    def wait_time(self) -> Optional[timedelta]:
        """
        Get the time taken until the task started running.

        :return: Time taken until task started running.
        """
        if self.start_time and self.ingest_time:
            return self.start_time - self.ingest_time
        return None

    def wait_time_once_unblocked(self) -> Optional[timedelta]:
        """
        Get the time taken until the task started running.

        Once it is unblocked by task dependencies.

        :return: Time taken until task started running.
        """
        if self.start_time and self.scheduled_time:
            return self.start_time - self.scheduled_time
        return None

    def is_success(self) -> bool:
        """
        Whether task was successful.

        :return: True if task was successful.
        """
        return self.status == EVG_SUCCESS_STATUS

    def is_undispatched(self) -> bool:
        """
        Whether the task was undispatched.

        :return: True is task was undispatched.
        """
        return self.status == EVG_UNDISPATCHED_STATUS

    def is_system_failure(self) -> bool:
        """
        Whether task resulted in a system failure.

        :return: True if task was a system failure.
        """
        if not self.is_success() and self.status_details and self.status_details.type:
            return self.status_details.type == EVG_SYSTEM_FAILURE_STATUS
        return False

    def is_timeout(self) -> bool:
        """
        Whether task results in a timeout.

        :return: True if task was a timeout.
        """
        if not self.is_success() and self.status_details and self.status_details.timed_out:
            return self.status_details.timed_out
        return False

    def is_active(self) -> bool:
        """
        Determine if the given task is active.

        :return: True if task is active.
        """
        return bool(self.scheduled_time and not self.finish_time)

    def __repr__(self) -> str:
        """
        Get a string representation of Task for debugging purposes.

        :return: String representation of Task.
        """
        return f"Task({self.task_id})"

    class Config:
        """Pydantic configuration for tasks."""

        extra = Extra.allow
