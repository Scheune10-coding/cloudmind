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