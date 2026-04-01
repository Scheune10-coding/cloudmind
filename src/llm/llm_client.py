import logging
import time

import requests

from src.config.config import Config
from src.llm.exceptions import AuthenticationError, LLMError, RateLimitError

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
REQUEST_TIMEOUT = 30


class LLMClient:
  def __init__(self):
    config = Config.get_instance()
    self.api_key = config.llm_api_key
    self.base_url = "https://api.openai.com/v1/chat/completions"
    self.model = config.llm_model
    self.max_tokens = config.llm_max_tokens
    self.temperature = config.llm_temperature
    self.system_prompt = config.llm_system_prompt

  def chat(self, messages: list) -> str:
    messages = [{"role": "system", "content": self.system_prompt}] + messages
    return self.call_api(messages, self.model, self.max_tokens)

  def call_api(self, messages: list, model: str, max_tokens: int = 1000) -> str:
    headers = {
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }

    body = {
      "model": model,
      "messages": messages,
      "max_tokens": max_tokens
    }

    last_exception = None
    for i in range(MAX_RETRIES):
      try:
        response = self.request(self.base_url, headers, body)
        usage = response.get("usage", {})
        logger.info(
          "Tokens -- prompt: %d, completion: %d, total: %d",
          usage.get("prompt_tokens", 0),
          usage.get("completion_tokens", 0),
          usage.get("total_tokens", 0),
        )
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")
      except AuthenticationError:
        raise
      except (RateLimitError, LLMError) as e:
        last_exception = e
        delay = (i + 1) ** 2
        logger.warning("LLM API error: %s. Retrying in %d seconds...", e, delay)
        time.sleep(delay)

    logger.error("Failed to call LLM API after %d attempts.", MAX_RETRIES)
    raise last_exception

  def request(self, url, headers, body):
    response = requests.post(url, headers=headers, json=body, timeout=REQUEST_TIMEOUT)
    if response.status_code == 401:
      raise AuthenticationError("LLM API authentication failed. Check your API key.")
    elif response.status_code == 429:
      raise RateLimitError("LLM API rate limit exceeded. Please try again later.")
    elif response.status_code != 200:
      raise LLMError(f"LLM API error: {response.status_code} - {response.text}")
    return response.json()
