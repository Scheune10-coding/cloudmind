from .request import Request
from .response import Response

class Router:
  def __init__(self):
    self.routes = {}
    self.paths = set()
    self.path_params = {}

  def add(self, method: str, path: str, handler):
    self.routes[f"{method}:{path}"] = handler
    self.paths.add(path)

  def dispatch(self, request: Request) -> Response:
    handler = self.routes.get(f"{request.method}:{request.path}")
    if handler:
      return handler(request)

    for key, handler in self.routes.items():
      method, pattern = key.split(':', 1)
      if method != request.method:
        continue
      params = self._match(pattern, request.path)
      if params is not None:
        request.path_params = params
        return handler(request)
      
    allowed_methods = []
    for key in self.routes.keys():
      method, pattern = key.split(':', 1)
      if self._match(pattern, request.path) is not None:
        allowed_methods.append(method)

    if allowed_methods:
      return Response.method_not_allowed({"error": "Method Not Allowed"}, allowed_methods)
    return Response.not_found({"error": "Not Found"})
      

  def _match(self, pattern: str, path: str) -> dict | None:
    pattern_parts = pattern.split('/')
    path_parts = path.split('/')

    if len(pattern_parts) != len(path_parts):
      return None
    
    params = {}
    for pattern_part, path_part in zip(pattern_parts, path_parts):
      if pattern_part.startswith('{') and pattern_part.endswith('}'):
        param_name = pattern_part[1:-1]
        params[param_name] = path_part
      elif pattern_part != path_part:
        return None
    return params
  