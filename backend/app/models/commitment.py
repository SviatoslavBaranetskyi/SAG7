from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
import enum


class CommitmentStatus(str, enum.Enum):
    to_check = "to_check"
    expired = "expired"
    done = "done"
    not_actual = "not_actual"
    ideas_backlog = "ideas_backlog"


class Commitment(Base):
    __tablename__ = "commitments"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    status: Mapped[str] = mapped_column(
        Enum(CommitmentStatus),
        default=CommitmentStatus.to_check,
    )

    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    project = relationship("Project", backref="commitments")