from src.app.chat.schemas import ChatResponse, CreateChatRequest
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
)
from openai import OpenAI


class ChatService:
    def __init__(self, openai_client: OpenAI):
        self.chat_client = openai_client

    def generate_response(self, chat_input: CreateChatRequest) -> ChatResponse:
        messages: list[ChatCompletionMessageParam] = [
            (
                ChatCompletionUserMessageParam(role="user", content=msg.content)
                if msg.role == "user"
                else ChatCompletionAssistantMessageParam(
                    role="assistant", content=msg.content
                )
            )
            for msg in (chat_input.messages or [])
        ]
        response = self.chat_client.chat.completions.create(
            model=chat_input.model,
            messages=messages,
        )
        message = response.choices[0].message
        return ChatResponse(message=message.content)
