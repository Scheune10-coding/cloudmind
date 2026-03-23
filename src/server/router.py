from .request import Request
from .response import Response

class Router:
  def __init__(self):
    self.routes = {}

  def add(self, method: str, path: str, handler):
    self.routes[f"{method}:{path}"] = handler

  def dispatch(self, request: Request) -> Response:
    handler = self.routes.get(f"{request.method}:{request.path}")
    if handler:
      return handler(request)
    return Response.not_found({"error": "Not Found"})