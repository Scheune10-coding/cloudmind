import sqlite3
from src.db.exceptions import NotFoundError, ValidationError
import pandas as pd
import logging
logger = logging.getLogger(__name__)

class Database:
  def __init__(self, db_path: str):
    self.db_path = db_path
    try:
      self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
      self.connection.row_factory = sqlite3.Row
      self.initialize()
    except Exception as e:
      logger.error(f"Error initializing database: {e}")
      raise e

  def initialize(self):
    self.connection.executescript('''
      CREATE TABLE IF NOT EXISTS users (
          id         INTEGER PRIMARY KEY AUTOINCREMENT,
          name       TEXT NOT NULL,
          created_at TEXT DEFAULT (datetime('now'))
      );

      CREATE TABLE IF NOT EXISTS sessions (
          id         INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id    INTEGER NOT NULL,
          title      TEXT,
          created_at TEXT DEFAULT (datetime('now')),
          FOREIGN KEY (user_id) REFERENCES users(id)
      );

      CREATE TABLE IF NOT EXISTS messages (
          id         INTEGER PRIMARY KEY AUTOINCREMENT,
          session_id INTEGER NOT NULL,
          role       TEXT NOT NULL,
          content    TEXT NOT NULL,
          created_at TEXT DEFAULT (datetime('now')),
          FOREIGN KEY (session_id) REFERENCES sessions(id)
      );
                                  
      ALTER TABLE sessions ADD COLUMN summary TEXT;
    ''')

  def create_user(self, name: str) -> int:
    cursor = self.connection.execute('INSERT INTO users (name) VALUES (?)', (name,))
    self.connection.commit()
    return cursor.lastrowid
    
  def get_user(self, user_id: int) -> dict:
    cursor = self.connection.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None
  
  def list_users(self) -> list:
    cursor = self.connection.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
  
  def create_session(self, user_id: int, title: str = None) -> dict:
    get_user = self.get_user(user_id)
    if not get_user:
      raise NotFoundError(f"User {user_id} not found")
    
    cursor = self.connection.execute('INSERT INTO sessions (user_id, title) VALUES (?, ?)', (user_id, title))
    self.connection.commit()
    return {"id": cursor.lastrowid}

  def get_session(self, session_id: int) -> dict:
    cursor = self.connection.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

  def list_sessions(self, user_id: int) -> list:
    cursor = self.connection.execute('SELECT * FROM sessions WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
  
  def add_summary(self, session_id: int, summary: str):
    cursor = self.connection.execute('UPDATE sessions SET summary = ? WHERE id = ?', (summary, session_id))
    self.connection.commit()
    return {"id": session_id}
  
  def add_message(self, session_id: int, role: str, content: str) -> dict:
    if role not in ['user', 'assistant']:
      raise ValidationError("Invalid role")
    cursor = self.connection.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)', (session_id, role, content))
    self.connection.commit()
    return {"id": cursor.lastrowid}
  
  def get_messages(self, session_id: int) -> list:
    cursor = self.connection.execute('SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC', (session_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
  
  def get_stats(self) -> dict:
    cursor = self.connection.execute('SELECT COUNT(*) AS user_count FROM users')
    user_count = cursor.fetchone()['user_count']
    
    cursor = self.connection.execute('SELECT COUNT(*) AS session_count FROM sessions')
    session_count = cursor.fetchone()['session_count']
    
    cursor = self.connection.execute('SELECT COUNT(*) AS message_count FROM messages')
    message_count = cursor.fetchone()['message_count']

    messages = self.get_messages_all()
    first_message = None
    last_message = None
    messages_per_role = {}
    if messages:
      df = pd.DataFrame(messages)
      df['created_at'] = pd.to_datetime(df['created_at'])
      
      first_message = df['created_at'].min().isoformat() if not df.empty else None
      last_message = df['created_at'].max().isoformat() if not df.empty else None
      messages_per_role = df['role'].value_counts().to_dict() if not df.empty else {}

    return {
      "users": user_count,
      "sessions": session_count,
      "messages": message_count,
      "first_message": first_message,
      "last_message": last_message,
      "messages_per_role": messages_per_role
    }
  
  def get_messages_all(self) -> list:
    cursor = self.connection.execute('SELECT * FROM messages ORDER BY created_at ASC')
    return [dict(row) for row in cursor.fetchall()]