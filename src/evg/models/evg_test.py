"""Models for evergreen test results."""
from datetime import datetime
from typing import List

from pydantic import BaseModel


class Log(BaseModel):
    """Evergreen test log model."""

    url: str
    line_num: int
    url_raw: str
    log_id: str


class EvgTest(BaseModel):
    """Evergreen test model."""

    task_id: str
    status: str
    test_file: str
    exit_code: int
    start_time: datetime
    end_time: datetime
    logs: List[Log]
