import requests
from src.config.config import Config
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

  def chat(self, messages: list) -> str:
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

    response = requests.post(self.base_url, headers=headers, json=body, timeout=30)
    data = response.json()
    usage = data.get("usage", {})
    logger.info(f"Tokens — prompt: {usage.get('prompt_tokens', 0)}, completion: {usage.get('completion_tokens', 0)}, total: {usage.get('total_tokens', 0)}")
    logger.info(f"Model: {data.get('model')}, finish_reason: {data.get('choices', [{}])[0].get('finish_reason')}")
    return data["choices"][0]["message"]["content"]

