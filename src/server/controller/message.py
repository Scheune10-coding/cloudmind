from src.server.request import Request
from src.server.response import Response
from src.db.database import Database


class MessageController:
  def __init__(self, database: Database):
    self.database = database

  def create(self, request: Request) -> Response:
    if not request.json:
      return Response.bad_request({"error": "Invalid JSON body"})
    session_id = request.path_params["id"]
    content = request.json.get("content")
    if not content:
      return Response.bad_request({"error": "Missing content"})
    message = self.database.add_message(session_id, "user", content)
    return Response.created(message)

  def list(self, request: Request) -> Response:
    session_id = request.path_params["id"]
    messages = self.database.get_messages(session_id)
    return Response.ok(messages)