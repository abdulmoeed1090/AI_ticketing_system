from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.services import chat_s as s
from src.security.deps import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat(request: ChatRequest,current_user=Depends(get_current_user)):
    return s.chat(
    current_user["id"],
    request.message
)


@router.get("/history")
def get_chat_history(
    current_user=Depends(get_current_user)
):
    return s.get_chat_history(
    current_user["id"]
)
    
    











