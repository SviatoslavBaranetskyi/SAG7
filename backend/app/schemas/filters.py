from pydantic import BaseModel
from app.models.commitment import CommitmentStatus


class CommitmentFilters(BaseModel):
    project_id: int | None = None
    reviewer_id: int | None = None
    status: CommitmentStatus | None = None