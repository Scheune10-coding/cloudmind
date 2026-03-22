from src.server.request import Request

def test_method_and_path():
  raw = "GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n"
  r = Request(raw)
  assert r.method == "GET"
  assert r.path == "/health"
  assert r.protocol == "HTTP/1.1"

def test_query_params():
  raw = "GET /health?debug=true HTTP/1.1\r\nHost: localhost\r\n\r\n"
  r = Request(raw)
  assert r.path == "/health"              # no ? in path
  assert r.query_params["debug"] == ["true"]

def test_headers():
  raw = "GET / HTTP/1.1\r\nHost: localhost\r\nX-Test: Hello\r\n\r\n"
  r = Request(raw)
  assert r.headers["Host"] == "localhost"
  assert r.headers["X-Test"] == "Hello"

def test_body_empty_on_get():
  raw = "GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n"
  r = Request(raw)
  assert r.body == ""

def test_body_on_post():
  raw = "POST /echo HTTP/1.1\r\nContent-Type: application/json\r\n\r\n{\"key\": \"value\"}"
  r = Request(raw)
  assert r.body == '{"key": "value"}'

def test_repr():
  raw = "GET /health HTTP/1.1\r\n\r\n"
  r = Request(raw)
  assert repr(r) == "REQUEST(GET /health)"