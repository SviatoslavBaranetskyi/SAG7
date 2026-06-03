from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db, get_current_user
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project import create_user_project, list_user_projects

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_user_project(
        db=db,
        name=payload.name,
        description=payload.description,
        owner_id=user.id,
    )


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return list_user_projects(db, user.id)