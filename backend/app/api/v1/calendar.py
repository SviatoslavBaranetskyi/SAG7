from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db, get_current_user
from app.repositories.commitment import get_commitments_by_user
from app.services.calendar import build_calendar_view

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/")
def get_calendar(
    project_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    commitments = get_commitments_by_user(db, user.id)

    if project_id:
        commitments = [
            c for c in commitments if c.project_id == project_id
        ]

    return build_calendar_view(commitments)