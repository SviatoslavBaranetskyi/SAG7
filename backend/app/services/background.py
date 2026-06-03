from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.commitment import Commitment, CommitmentStatus


def expire_commitments_job():
    db: Session = SessionLocal()

    try:
        now = datetime.now(timezone.utc)

        commitments = db.query(Commitment).filter(
            Commitment.status == CommitmentStatus.to_check,
            Commitment.deadline < now,
        ).all()

        for c in commitments:
            c.status = CommitmentStatus.expired

        db.commit()

    finally:
        db.close()