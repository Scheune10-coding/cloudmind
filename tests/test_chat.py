import pytest
from unittest.mock import MagicMock
from src.db.database import Database
from src.server.controller.chat import ChatController


@pytest.fixture
def db(tmp_path):
    return Database(str(tmp_path / "test.db"))


@pytest.fixture
def session(db):
    user_id = db.create_user("Test User")
    return db.create_session(user_id, "Test Session")


@pytest.fixture
def controller(db):
    mock_llm = MagicMock()
    mock_llm.chat.return_value = "Ich bin CloudMind"
    return ChatController(db, mock_llm)


def test_chat_missing_message_field(controller):
    request = MagicMock()
    request.json = {"session_id": 1}
    response = controller.create(request)
    assert response.status == 400


def test_chat_missing_session_id(controller):
    request = MagicMock()
    request.json = {"message": "Hallo"}
    response = controller.create(request)
    assert response.status == 400


def test_chat_session_not_found(controller):
    request = MagicMock()
    request.json = {"session_id": 999, "message": "Hallo"}
    response = controller.create(request)
    assert response.status == 404


def test_chat_saves_both_messages(db, session, controller):
    request = MagicMock()
    request.json = {"session_id": session["id"], "message": "Wer bist du?"}
    controller.create(request)
    messages = db.get_messages(session["id"])
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Wer bist du?"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "Ich bin CloudMind"


def test_chat_llm_called_with_correct_message(db, session):
    mock_llm = MagicMock()
    mock_llm.chat.return_value = "Antwort"
    controller = ChatController(db, mock_llm)
    request = MagicMock()
    request.json = {"session_id": session["id"], "message": "Test"}
    controller.create(request)
    mock_llm.chat.assert_called_once_with([{"role": "user", "content": "Test"}])


def test_chat_no_api_call_on_invalid_request(db):
    mock_llm = MagicMock()
    controller = ChatController(db, mock_llm)
    request = MagicMock()
    request.json = {}
    controller.create(request)
    mock_llm.chat.assert_not_called()