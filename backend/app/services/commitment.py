from sqlalchemy.orm import Session

from app.repositories.commitment import (
    create_commitment,
    get_commitments_by_project,
)


def create_new_commitment(db: Session, data: dict, author_id: int):
    return create_commitment(db, data, author_id)


def list_project_commitments(db: Session, project_id: int):
    return get_commitments_by_project(db, project_id)