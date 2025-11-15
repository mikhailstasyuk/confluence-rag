from fastapi.testclient import TestClient
from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
)
from openai.types.chat.chat_completion import Choice
import pytest
from pytest_mock import MockerFixture

from src.app.main import app
from src.app.chat.service import ChatService
from src.app.chat.schemas import ChatResponse

client = TestClient(app)


@pytest.fixture
def mock_openai_client(mocker: MockerFixture) -> OpenAI:
    client = mocker.Mock(spec=OpenAI)
    client.chat = mocker.Mock()
    client.chat.completions = mocker.Mock()
    return client


@pytest.fixture
def mock_service(mock_openai_client: OpenAI) -> ChatService:
    return ChatService(
        openai_client=mock_openai_client
    )


def test_chat_service_calls_openai(
        mock_service: ChatService,
        mock_openai_client: OpenAI,
        mocker: MockerFixture,
)-> None:
    mock_completion = ChatCompletion(
        id="test-id",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content="This is a model response",
                    role="assistant",
                ),
            )
        ],
        created=1234567890,
        model="gpt-5",
        object="chat.completion",
    )
    mock_create_completion = mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mock_completion
    )
    response = mock_service.generate_response(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )
    mock_create_completion.assert_called_once()


def test_chat_service_passes_messages_and_model(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
):
    mock_create = mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content="ok"))])
    )
    mock_service.generate_response(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )
    mock_create.assert_called_once_with(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )

def test_chat_service_returns_chat_response_object(
        mock_service: ChatService,
        mock_openai_client: OpenAI,
        mocker: MockerFixture,
)-> None:
    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content="ok"))]
        )
    )
    response = mock_service.generate_response(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )
    assert isinstance(response, ChatResponse)
    