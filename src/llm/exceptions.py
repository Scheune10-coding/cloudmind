class LLMError(Exception):
  pass

class RateLimitError(LLMError):
  pass

class AuthenticationError(LLMError):
  pass