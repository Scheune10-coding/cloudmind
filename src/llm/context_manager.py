import logging

from src.config.config import Config

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

  if kept and kept[0]["role"] != "user":
      kept.insert(0, rest[-1])

  trimmed = len(rest) - len(kept)
  if trimmed > 0:
      logger.debug("Context trimmed from %d to %d messages", len(rest), len(kept))

  return system + kept