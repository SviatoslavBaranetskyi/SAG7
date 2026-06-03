from sqlalchemy.orm import Session

from app.models.commitment import Commitment, CommitmentStatus
from app.services.commitment_status import resolve_status


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