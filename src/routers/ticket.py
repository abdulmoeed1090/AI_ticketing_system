from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.services import ticket_s as s
from src.security.deps import get_current_user, require_roles

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketUpdate(BaseModel):
    title: str
    description: str
    status: str


@router.get("/")
def get_all_tickets(
    current_user=Depends(get_current_user)
):
    return s.get_all_tickets()


@router.get("/{ticket_id}")
def get_ticket(
    ticket_id: int,
    current_user=Depends(get_current_user)
):
    return s.get_ticket(ticket_id)


@router.post("/")
def create_ticket(
    ticket: TicketCreate,
    current_user=Depends(require_roles("customer"))
):
    return s.create_ticket(
    ticket.title,
    ticket.description,
    current_user["id"]
)


@router.put("/{ticket_id}")
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    current_user=Depends(require_roles("agent"))
):
    return s.update_ticket(
        ticket_id,
        ticket.title,
        ticket.description,
        ticket.status
    )


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    current_user=Depends(require_roles("admin"))
):
    return s.delete_ticket(ticket_id)