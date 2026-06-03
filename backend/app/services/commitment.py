from sqlalchemy.orm import Session

from app.schemas.filters import CommitmentFilters
from app.services.permissions import check_commitment_access
from app.repositories.commitment import (
    create_commitment,
    update_commitment,
    delete_commitment,
    update_status,
    get_commitments_by_project,
    update_commitment_status,
    get_filtered_commitments,
)


def create_new_commitment(db: Session, data: dict, author_id: int):
    return create_commitment(db, data, author_id)


def list_project_commitments(db: Session, project_id: int):
    return get_commitments_by_project(db, project_id)


def list_project_commitments(db, project_id: int):
    commitments = get_commitments_by_project(db, project_id)

    for c in commitments:
        update_commitment_status(db, c)

    return commitments


def list_filtered_commitments(db, user_id: int, filters: CommitmentFilters):
    return get_filtered_commitments(db, user_id, filters)


def update_existing_commitment(db, user, commitment, data):
    check_commitment_access(user, commitment)
    return update_commitment(db, commitment, data)


def delete_existing_commitment(db, user, commitment):
    check_commitment_access(user, commitment)
    return delete_commitment(db, commitment)


def change_commitment_status(db, user, commitment, status):
    check_commitment_access(user, commitment)
    return update_status(db, commitment, status)
