import requests
from src.config.config import Config
from src.llm.exceptions import AuthenticationError, RateLimitError, LLMError
import time
import logging
logger = logging.getLogger(__name__)


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

  def complete(self, system_prompt: str, user_input: str) -> str:
    messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_input}
    ]
    return self.call_api(messages, self.model, self.max_tokens)

  def call_api(self, messages: list, model: str, max_tokens: int = 1000):
    headers = {
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    }

    body = {
      "model": model,
      "messages": messages,
      "max_tokens": max_tokens
    }

    response = {}
    for i in range(3):
      try:
        response = self.request(self.base_url, headers, body)
      except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        break
      except RateLimitError as e:
        logger.warning(f"Rate limit error: {e}. Retrying in {i ** 2} seconds...")
        time.sleep(i ** 2)
        continue
      except LLMError as e:
        logger.warning(f"LLM API error: {e}. Retrying in {i ** 2} seconds...")
        time.sleep(i ** 2)
        continue
      if i == 2:
        logger.error("Failed to call LLM API after 3 attempts.")
      break
    
    usage = response.get("usage", {})
    logger.info(f"Tokens — prompt: {usage.get('prompt_tokens', 0)}, completion: {usage.get('completion_tokens', 0)}, total: {usage.get('total_tokens', 0)}")
    response_message = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    return response_message

  def request(self, url, headers, body, timeout=30):
    response = requests.post(url, headers=headers, json=body, timeout=timeout)
    if response.status_code == 401:
      raise AuthenticationError("LLM API authentication failed. Check your API key.")
    elif response.status_code == 429:
      raise RateLimitError("LLM API rate limit exceeded. Please try again later.")
    elif response.status_code != 200:
      raise LLMError(f"LLM API error: {response.status_code} - {response.text}")
    return response.json()

