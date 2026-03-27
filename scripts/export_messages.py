from src.db.database import Database
import pandas as pd
from src.config.config import Config
import time
import os

config = Config.load("config.yaml")
db = Database(config.database_path)
cursor = db.connection.execute('''
  SELECT m.id, m.session_id, m.role, m.content, m.created_at, s.user_id
  FROM messages m
  JOIN sessions s ON m.session_id = s.id
''')
rows = cursor.fetchall()

messages = []
for row in rows:
  messages.append({
    "id": row["id"],
    "session_id": row["session_id"],
    "role": row["role"],
    "content": row["content"],
    "created_at": row["created_at"],
    "user_id": row["user_id"]
  })

df = pd.DataFrame(messages)
os.makedirs("data", exist_ok=True)
df.to_csv(f"data/messages_export_{time.strftime('%Y-%m-%d')}.csv", index=False)