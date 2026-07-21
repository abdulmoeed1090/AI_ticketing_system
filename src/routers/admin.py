from fastapi import APIRouter, Depends

from src.services import admin_s as s
from src.security.deps import require_roles

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users")
def get_users(
    current_user=Depends(require_roles("admin"))
):
    return s.get_users()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user=Depends(require_roles("admin"))
):
    return s.delete_user(user_id)


@router.put("/assign-ticket/{ticket_id}/{agent_id}")
def assign_ticket(
    ticket_id: int,
    agent_id: int,
    current_user=Depends(require_roles("admin"))
):
    return s.assign_ticket(
        ticket_id,
        agent_id
    )