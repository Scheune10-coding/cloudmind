from src.server.response import Response

def test_response_ok():
  response = Response.ok({"message": "Success"})
  assert response.status == 200
  assert response.body == {"message": "Success"}

def test_response_not_found():
  response = Response.not_found({"error": "Not Found"})
  assert response.status == 404
  assert response.body == {"error": "Not Found"}


def test_response_to_bytes():
  response = Response.ok({"message": "Success"})
  b = response.to_bytes()
  assert b"HTTP/1.1 200 OK" in b
  assert b"Content-Type: application/json" in b
  assert b"Content-Length:" in b
  assert b'"message"' in b
  assert b'"Success"' in b
