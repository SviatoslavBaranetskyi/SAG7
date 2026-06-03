from sqlalchemy.orm import Session

from app.repositories.project import create_project, get_projects_by_user


def create_user_project(db: Session, name: str, description: str, owner_id: int):
    return create_project(db, name, description, owner_id)


def list_user_projects(db: Session, owner_id: int):
    return get_projects_by_user(db, owner_id)