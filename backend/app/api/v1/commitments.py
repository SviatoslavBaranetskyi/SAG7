from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db, get_current_user
from app.schemas.filters import CommitmentFilters
from app.schemas.commitment import CommitmentCreate, CommitmentResponse
from app.services.commitment import (
    create_new_commitment,
    list_project_commitments,
    list_filtered_commitments,
)

router = APIRouter(prefix="/commitments", tags=["commitments"])


@router.post("/", response_model=CommitmentResponse)
def create(
    payload: CommitmentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_new_commitment(
        db=db,
        data=payload.dict(),
        author_id=user.id,
    )


@router.get("/{project_id}", response_model=list[CommitmentResponse])
def list_commitments(
    project_id: int,
    db: Session = Depends(get_db),
):
    return list_project_commitments(db, project_id)


@router.get("/")
def list_commitments(
    project_id: int | None = Query(None),
    reviewer_id: int | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    filters = CommitmentFilters(
        project_id=project_id,
        reviewer_id=reviewer_id,
        status=status,
    )

    return list_filtered_commitments(db, user.id, filters)