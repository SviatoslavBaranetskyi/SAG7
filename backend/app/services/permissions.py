from fastapi import HTTPException, status


def check_commitment_access(user, commitment):
    if user.id in [
        commitment.author_id,
        commitment.assignee_id,
        commitment.reviewer_id,
    ]:
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No access to this commitment",
    )