from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel


class BuildVariantsStatus(BaseModel):

    build_variant: str
    build_id: str


class EvgVersion(BaseModel):

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
    # parameters: List[]
    build_variants_status: List[BuildVariantsStatus]
    requester: str
    # errors: List[]

    def build_map(self) -> Dict[str, str]:
        return {bv.build_variant: bv.build_id for bv in self.build_variants_status}
