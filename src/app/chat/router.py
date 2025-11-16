from fastapi import APIRouter, Depends

from src.app.chat.schemas import ChatResponse
from src.app.chat.dependencies import get_chat_service
from src.app.chat.service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=[
        "Chat",
    ],
)


@router.post("")
async def chat(service: ChatService = Depends(get_chat_service)):
    return ChatResponse(message="Hello Kitty")
