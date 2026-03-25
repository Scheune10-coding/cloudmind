from src.db.database import Database
from src.server.request import Request
from src.server.response import Response

class UserController:
  def __init__(self, database: Database):
    self.database = database

  def create(self, request: Request) -> Response:
    if not request.json:
      return Response.bad_request({"error": "Invalid JSON body"})
    name = request.json.get("name")
    if not name:
      return Response.bad_request({"error": "Missing name"})
    user_id = self.database.create_user(name)
    return Response.created({"id": user_id})

  def get(self, request: Request) -> Response:
    user_id = request.path_params["id"]
    user = self.database.get_user(user_id)
    return Response.ok(user) if user else Response.not_found({"error": "User not found"})

  def list(self, request: Request) -> Response:
    users = self.database.list_users()
    return Response.ok(users) if users else Response.not_found({"error": "No users found"})
