class TokenTracker:
  def __init__(self):
    self.sessions = {}
    self.total_prompt = 0
    self.total_completion = 0

  def add(self, session_id: str, prompt_tokens: int, completion_tokens: int):
    if session_id not in self.sessions:
      self.sessions[session_id] = {"prompt": 0, "completion": 0}
    self.sessions[session_id]["prompt"] += prompt_tokens
    self.sessions[session_id]["completion"] += completion_tokens
    self.total_prompt += prompt_tokens
    self.total_completion += completion_tokens

  def get_cost(self):
    input_cost = (self.total_prompt / 1_000_000) * 0.15
    output_cost = (self.total_completion / 1_000_000) * 0.60
    return input_cost + output_cost
