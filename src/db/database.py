import sqlite3

class Database:
  def __init__(self, db_path: str):
    self.db_path = db_path
    self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
    self.connection.row_factory = sqlite3.Row
    self.initialize()

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