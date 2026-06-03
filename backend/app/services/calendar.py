from collections import defaultdict
from datetime import date

from app.models.commitment import CommitmentStatus


def build_calendar_view(commitments):
    calendar = defaultdict(list)

    for c in commitments:
        day = c.deadline.date()

        calendar[day].append(
            {
                "id": c.id,
                "title": c.title,
                "status": c.status,
                "project_id": c.project_id,
                "deadline": c.deadline,
            }
        )

    for day in calendar:
        calendar[day].sort(key=lambda x: x["deadline"])

    return dict(calendar)