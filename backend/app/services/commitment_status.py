from datetime import datetime, timezone

from app.models.commitment import CommitmentStatus


def resolve_status(current_status: str, deadline: datetime) -> str:
    if current_status in [
        CommitmentStatus.done,
        CommitmentStatus.not_actual,
        CommitmentStatus.ideas_backlog,
    ]:
        return current_status

    now = datetime.now(timezone.utc)

    if deadline < now:
        return CommitmentStatus.expired

    return CommitmentStatus.to_check