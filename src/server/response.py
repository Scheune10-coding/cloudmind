import json

STATUS = {
  200: 'OK',
  400: 'Bad Request',
  404: 'Not Found',
  500: 'Internal Server Error'
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