import logging

from src.config.config import Config
from src.llm.llm_client import LLMClient

logger = logging.getLogger(__name__)

def count_tokens(messages: list) -> int:
  return sum(len(message["content"])//4 for message in messages)

def trim_context(messages: list, max_tokens: int) -> list:
  system = [m for m in messages if m["role"] == "system"]
  rest   = [m for m in messages if m["role"] != "system"]

  kept = []
  current_tokens = 0

  for message in reversed(rest):
      message_tokens = len(message["content"]) // 4
      if current_tokens + message_tokens > max_tokens:
          break
      kept.insert(0, message)
      current_tokens += message_tokens

  trimmed = len(rest) - len(kept)
  if trimmed > 0:
      logger.debug("Context trimmed from %d to %d messages", len(rest), len(kept))

  return system + kept

def summarize_context(messages: list, llm_client: LLMClient) -> dict:
  context = "\n".join([m["content"] for m in messages])
  summarize_messages = {"role": "user", "content": f"Summarize the following conversation in less than 3 sentences:\n{context}"}
  summary = llm_client.chat([summarize_messages])
  response = {"role": "system", "content": f"Kontext: {summary}"}
  return response