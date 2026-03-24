from src.server.router import Router
from src.server.request import Request
from src.server.response import Response


router = Router()

def hello_handler(request: Request) -> Response:
    return Response.ok({"message": "Hello, World!"})

router.add("GET", "/hello", hello_handler)


def test_router_dispatch():
  request = Request("GET /hello HTTP/1.1\r\nHost: localhost\r\n\r\n")
  response = router.dispatch(request)
  
  assert response.status == 200
  assert response.body == {"message": "Hello, World!"}

def test_not_found():
  request = Request("GET /notfound HTTP/1.1\r\nHost: localhost\r\n\r\n")
  response = router.dispatch(request)
  
  assert response.status == 404
  assert response.body == {"error": "Not Found"}

def test_method_not_allowed():
  request = Request("POST /hello HTTP/1.1\r\nHost: localhost\r\n\r\n")
  response = router.dispatch(request)

  assert response.status == 405
  assert response.body == {"error": "Method Not Allowed"}