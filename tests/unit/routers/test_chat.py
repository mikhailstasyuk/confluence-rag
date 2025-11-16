from fastapi.testclient import TestClient

from src.app.chat.schemas import ChatResponse

payload = {
    "model": "test-model", 
    "messages": [
        {"role": "user", "message": "Hi"},
        {"role": "assistant", "message": "Hello"},
        {"role": "user", "message": "What is molasses?"},
    ]
}


def test_chat_available(client_with_mock_service: TestClient):
    response = client_with_mock_service.post("/chat", json=payload)
    assert response.status_code == 200


def test_chat_returns_chat_response(client_with_mock_service: TestClient):
    response = client_with_mock_service.post("/chat", json=payload)
    chat_response = ChatResponse(**response.json())
    assert chat_response.message == "Hello Kitty"
