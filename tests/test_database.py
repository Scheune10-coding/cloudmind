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
  retrieved_session = db.get_session(session_id, user_id)
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
