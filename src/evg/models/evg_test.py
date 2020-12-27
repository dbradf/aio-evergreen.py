"""Test representation of evergreen."""
from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class EvgTestLogs(BaseModel):
    """Representation of test logs from evergreen."""

    url: Optional[str]
    line_num: int
    url_raw: Optional[str]
    log_id: Optional[str]


class EvgTest(BaseModel):
    """Representation of a test object from evergreen."""

    task_id: str
    status: str
    test_file: str
    exit_code: int
    start_time: datetime
    end_time: Optional[datetime]
    logs: EvgTestLogs
