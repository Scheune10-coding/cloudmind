import socket
import threading
import sys
from src.server.request import Request
from src.server.response import Response
from src.server.router import Router

# Router instanziieren und Routen registrieren
router = Router()

def health_handler(request: Request) -> Response:
    return Response.ok({"status": "ok"})

def home_handler(request: Request) -> Response:
    return Response.ok({"message": "Willkommen bei CloudMind"})

router.add("GET", "/health", health_handler)
router.add("GET", "/", home_handler)

def handle_connection(conn, addr):
  print(f"Connection from {addr}")
  try:
    request_data = conn.recv(1024).decode('utf-8')
    request = Request(request_data)
    response = router.dispatch(request)
    conn.sendall(response.to_bytes())
  except Exception as e:
    print(f"[ERROR]: {e}", file=sys.stderr)
    conn.sendall(Response.error(str(e)))
  finally:
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 8080))
server.listen(5)
print("Server is listening on port 8080...")

while True:
    conn = None
    try:
        conn, addr = server.accept()
        threading.Thread(target=handle_connection, args=(conn, addr)).start()
    except Exception as e:
        print(f"[ERROR]: {e}", file=sys.stderr)   