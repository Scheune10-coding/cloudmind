import logging

from src.db.database import Database
from src.llm.llm_client import LLMClient
from src.server.request import Request
from src.server.response import Response
from src.llm.context_manager import count_tokens, trim_context, summarize_context

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

    
    messages = self.database.get_messages(session_id)
    user_message = {"role": "user", "content": request.json["message"]}
    llm_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    if count_tokens(llm_messages) >= self.llm_client.context_max_tokens*0.8:
      context_message = summarize_context(self.database.get_messages(session_id), self.llm_client)
      self.database.add_summary(session_id, context_message["content"])
    else:
      context_message = None
    llm_messages.append(user_message)
    if context_message:
      llm_messages.insert(0, context_message)
    response_message = self.llm_client.chat(trim_context(llm_messages, self.llm_client.context_max_tokens))
    if not response_message:
      return Response.error("LLM did not return a response")

    message_id = self.database.add_message(session["id"], user_message["role"], user_message["content"])["id"]
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
