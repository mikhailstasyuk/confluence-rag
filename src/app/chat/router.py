from fastapi import APIRouter, Depends, HTTPException

from src.app.chat.schemas import CreateChatRequest
from src.app.chat.dependencies import get_chat_service
from src.app.chat.service import ChatService
from src.app.chat.exceptions import ChatServiceError

router = APIRouter(
    prefix="/chat",
    tags=[
        "Chat",
    ],
)


@router.post("")
async def chat(
    chat_input: CreateChatRequest, service: ChatService = Depends(get_chat_service)
):
    try:
        return service.generate_response(chat_input)
    except ChatServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ValueError as e:
        # Catches configuration errors like missing API key
        raise HTTPException(status_code=503, detail=str(e))
