import urllib.parse
import json

class Request:
  def __init__(self, raw: str):
    self.raw = raw

    # Parse the request line
    self.method, self.path, self.protocol = raw.split('\n')[0].split()

    # Parse the query parameters
    raw_path = self.path
    self.path = raw_path.split('?')[0]
    self.path_params: dict = {}
    self.query_params = urllib.parse.parse_qs(raw_path.split('?')[1]) if '?' in raw_path else {}
    
    # Parse the headers
    self.headers = {
      key: value.strip()
      for header in raw.split('\n')[1:]
      if ': ' in header
      for key, value in [header.split(': ', 1)]
    }
    
    # Parse the body
    self.body: str = self.raw.split('\r\n\r\n', 1)[1] if '\r\n\r\n' in self.raw else ''
    try:
        self.json = json.loads(self.body) if self.headers.get('Content-Type') == 'application/json' else None
    except json.JSONDecodeError:
        self.json = None

  def __repr__(self):
    return f"REQUEST({self.method} {self.path})"