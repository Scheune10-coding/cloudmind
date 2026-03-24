import json

STATUS = {
  200: 'OK',
  201: 'Created',
  202: 'Accepted',
  400: 'Bad Request',
  401: 'Unauthorized',
  403: 'Forbidden',
  404: 'Not Found',
  405: 'Method Not Allowed',
  408: 'Request Timeout',
  500: 'Internal Server Error',
  501: 'Not Implemented',
  502: 'Bad Gateway'
}

class Response:
  def __init__ (self, status: int, body: dict):
    self.status = status
    self.body = body

  def to_bytes (self) -> bytes:
    body_bytes = json.dumps(self.body).encode('utf-8')
    status_line = f'HTTP/1.1 {self.status} {STATUS[self.status]}\r\n'
    headers = f'Content-Type: application/json\r\nContent-Length: {len(body_bytes)}\r\n\r\n'
    return (status_line + headers).encode('utf-8') + body_bytes
  
  @classmethod
  def ok (cls, body: dict) -> 'Response':
    return cls(200, body)
  
  @classmethod
  def not_found (cls, body: dict) -> 'Response':
    return cls(404, body)
  
  @classmethod
  def error (cls, message: str) -> 'Response':
    return cls(500, {"error": message})