import pytest
from src.db.database import Database

@pytest.fixture
def db(tmp_path):
  return Database(str(tmp_path / "test.db"))

def test_create_user(db):
  user_id = db.create_user("Test User")
  assert isinstance(user_id, int)

def test_get_user(db):
  user_id = db.create_user("Test User")
  user = db.get_user(user_id)
  assert user['name'] == "Test User"

def test_list_users(db):
  db.create_user("Test User")
  users = db.list_users()
  assert isinstance(users, list)
  assert len(users) > 0

def test_create_session(db):
  user_id = db.create_user("Test User")
  session = db.create_session(user_id, "Test Session")
  assert "id" in session
  assert session["id"] == 1

def test_get_session(db):
  user_id = db.create_user("Test User")
  session = db.create_session(user_id, "Test Session")
  session_id = session["id"]
  retrieved_session = db.get_session(session_id)
  assert retrieved_session is not None
  assert retrieved_session["id"] == session_id
  assert retrieved_session["user_id"] == user_id

def test_list_sessions(db):
  user_id = db.create_user("Test User")
  db.create_session(user_id, "Test Session 1")
  db.create_session(user_id, "Test Session 2")
  sessions = db.list_sessions(user_id)
  assert isinstance(sessions, list)
  assert len(sessions) == 2

def test_add_message(db):
  user_id = db.create_user("Test User")
  session = db.create_session(user_id, "Test Session")
  session_id = session["id"]
  message = db.add_message(session_id, "user", "Hello, world!")
  assert "id" in message

def test_get_messages(db):
  user_id = db.create_user("Test User")
  session = db.create_session(user_id, "Test Session")
  session_id = session["id"]
  db.add_message(session_id, "user", "Hello, world!")
  messages = db.get_messages(session_id)
  assert isinstance(messages, list)
  assert len(messages) == 1
  assert messages[0]["session_id"] == session_id
  assert messages[0]["role"] == "user"
  assert messages[0]["content"] == "Hello, world!"

def test_get_stats(db):
  user_id = db.create_user("Test User")
  session = db.create_session(user_id, "Test Session")
  session_id = session["id"]
  db.add_message(session_id, "user", "Hello, world!")
  stats = db.get_stats()
  assert stats["users"] == 1
  assert stats["sessions"] == 1
  assert stats["messages"] == 1
  assert stats["first_message"] is not None
  assert stats["last_message"] is not None
  assert isinstance(stats["messages_per_role"], dict)
