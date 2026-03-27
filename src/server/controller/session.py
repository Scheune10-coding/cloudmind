from src.server.request import Request
from src.server.response import Response
from src.db.database import Database
import logging
logger = logging.getLogger(__name__)

class SessionController:
  def __init__(self, database: Database):
    self.database = database

  def create(self, request: Request) -> Response:
    if not request.json:
      logger.warning("create_session: missing JSON-Body")
      return Response.bad_request({"error": "Invalid JSON body"})
    user_id = request.json.get("user_id")
    title = request.json.get("title")
    if not user_id:
      logger.warning("create_session: missing user_id")
      return Response.bad_request({"error": "Missing user_id"})
    if not title:
      logger.warning("create_session: missing title")
      return Response.bad_request({"error": "Missing title"})
    try:
      session = self.database.create_session(user_id, title)
    except ValueError:
      return Response.bad_request({"error": "Invalid user_id"})
    return Response.created(session)

  def get(self, request: Request) -> Response:
    session_id = request.path_params["id"]
    session = self.database.get_session(session_id)
    if not session:
      logger.warning(f"get_session: session {session_id} not found")
      return Response.not_found({"error": "Session not found"})
    return Response.ok(session)

  def list(self, request: Request) -> Response:
    user_id = request.path_params["id"]
    sessions = self.database.list_sessions(user_id)
    return Response.ok(sessions) if sessions else Response.not_found({"error": "No sessions found"})