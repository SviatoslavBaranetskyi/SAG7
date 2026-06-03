from sqlalchemy.orm import Session

from app.models.commitment import Commitment, CommitmentStatus


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