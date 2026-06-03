from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.commitment import Commitment, CommitmentStatus
from app.services.commitment_status import resolve_status
from app.schemas.filters import CommitmentFilters


def create_commitment(db: Session, data: dict, author_id: int):
    commitment = Commitment(
        **data,
        author_id=author_id,
        status=CommitmentStatus.to_check,
    )

    db.add(commitment)
    db.commit()
    db.refresh(commitment)

    return commitment


def get_commitments_by_project(db: Session, project_id: int):
    return db.query(Commitment).filter(
        Commitment.project_id == project_id
    ).all()


def update_commitment_status(db, commitment):
    commitment.status = resolve_status(
        commitment.status,
        commitment.deadline,
    )

    db.commit()
    db.refresh(commitment)

    return commitment


def get_commitments_by_user(db, user_id: int):
    return db.query(Commitment).filter(
        (Commitment.author_id == user_id) |
        (Commitment.assignee_id == user_id) |
        (Commitment.reviewer_id == user_id)
    ).all()


def get_filtered_commitments(
    db: Session,
    user_id: int,
    filters: CommitmentFilters,
):
    query = select(Commitment).where(
        (Commitment.author_id == user_id)
        | (Commitment.assignee_id == user_id)
        | (Commitment.reviewer_id == user_id)
    )

    if filters.project_id:
        query = query.where(Commitment.project_id == filters.project_id)

    if filters.reviewer_id:
        query = query.where(Commitment.reviewer_id == filters.reviewer_id)

    if filters.status:
        query = query.where(Commitment.status == filters.status)

    return db.execute(query).scalars().all()