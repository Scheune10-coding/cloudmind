from src.server.request import Request
from src.server.response import Response
from src.db.database import Database

class SessionController:
  def __init__(self, database: Database):
    self.database = database

  def create(self, request: Request) -> Response:
    if not request.json:
      return Response.bad_request({"error": "Invalid JSON body"})
    user_id = request.json.get("user_id")
    title = request.json.get("title")
    if not user_id:
      return Response.bad_request({"error": "Missing user_id"})
    if not title:
      return Response.bad_request({"error": "Missing title"})
    try:
      session = self.database.create_session(user_id, title)
    except ValueError:
      return Response.bad_request({"error": "Invalid user_id"})
    return Response.created(session)

  def get(self, request: Request) -> Response:
    session_id = request.path_params["id"]
    session = self.database.get_session(session_id)
    return Response.ok(session) if session else Response.not_found({"error": "Session not found"})

  def list(self, request: Request) -> Response:
    user_id = request.path_params["id"]
    sessions = self.database.list_sessions(user_id)
    return Response.ok(sessions) if sessions else Response.not_found({"error": "No sessions found"})