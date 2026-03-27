from src.db.database import Database
from src.server.request import Request
from src.server.response import Response
import logging
logger = logging.getLogger(__name__)

class UserController:
  def __init__(self, database: Database):
    self.database = database

  def create(self, request: Request) -> Response:
    if not request.json:
      logger.warning("create_user: missing JSON-Body")
      return Response.bad_request({"error": "Invalid JSON body"})
    name = request.json.get("name")
    if not name:
      logger.warning("create_user: missing name")
      return Response.bad_request({"error": "Missing name"})
    user_id = self.database.create_user(name)
    return Response.created({"id": user_id})

  def get(self, request: Request) -> Response:
    user_id = request.path_params["id"]
    user = self.database.get_user(user_id)
    if not user:
      logger.warning(f"get_user: user {user_id} not found")
      return Response.not_found({"error": "User not found"})
    return Response.ok(user)

  def list(self, request: Request) -> Response:
    users = self.database.list_users()
    return Response.ok(users) if users else Response.not_found({"error": "No users found"})
