import logging

from src.db.database import Database
from src.llm.llm_client import LLMClient
from src.server.request import Request
from src.server.response import Response

logger = logging.getLogger(__name__)


class ChatController:
  def __init__(self, database: Database, llm_client: LLMClient):
    self.database = database
    self.llm_client = llm_client

  def create(self, request: Request) -> Response:
    if not request.json or "message" not in request.json:
      return Response.bad_request({"error": "Invalid JSON body, expected 'message' field"})
    session_id = request.json.get("session_id")
    if not session_id:
      return Response.bad_request({"error": "Session ID is required"})
    session = self.database.get_session(session_id)
    if not session:
      return Response.not_found({"error": "Session not found"})

    message = request.json["message"]
    response_message = self.llm_client.chat([{"role": "user", "content": message}])
    if not response_message:
      return Response.error("LLM did not return a response")

    message_id = self.database.add_message(session["id"], "user", message)["id"]
    response_message_id = self.database.add_message(session["id"], "assistant", response_message)["id"]
    logger.info(
      "LLM response saved. message_id=%s, response_id=%s",
      message_id, response_message_id,
    )
    return Response.ok({
      "reply": response_message,
      "session_id": session["id"],
      "message_id": response_message_id,
    })
