from sqlalchemy.orm import Session

from app.models.project import Project


def create_project(db: Session, name: str, description: str | None, owner_id: int):
    project = Project(
        name=name,
        description=description,
        owner_id=owner_id,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects_by_user(db: Session, owner_id: int):
    return db.query(Project).filter(Project.owner_id == owner_id).all()