from datetime import datetime
from pydantic import BaseModel

from app.models.commitment import CommitmentStatus


class CommitmentCreate(BaseModel):
    title: str
    description: str | None = None

    project_id: int

    assignee_id: int
    reviewer_id: int

    deadline: datetime


class CommitmentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: CommitmentStatus
    deadline: datetime

    class Config:
        from_attributes = True