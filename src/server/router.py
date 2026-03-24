from .request import Request
from .response import Response

class Router:
  def __init__(self):
    self.routes = {}
    self.paths = set()

  def add(self, method: str, path: str, handler):
    self.routes[f"{method}:{path}"] = handler
    self.paths.add(path)

  def dispatch(self, request: Request) -> Response:
    keys = self.routes.keys()
    allowed_methods = []
    for key in keys:
      if key.split(':', 1)[1] == request.path:
        allowed_methods.append(key.split(':')[0])

    handler = self.routes.get(f"{request.method}:{request.path}")
    if handler:
      return handler(request)
    else:
      if request.path in self.paths:
        return Response.method_not_allowed({"error": "Method Not Allowed"}, allowed_methods)
      else:
        return Response.not_found({"error": "Not Found"})