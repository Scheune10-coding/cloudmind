import socket
import threading
import sys
from src.server.request import Request
from src.server.response import Response
from src.server.router import Router
from src.db.database import Database

# Router instanziieren und Routen registrieren
router = Router()
database = Database('data/cloudmind.db')

def health_handler(request: Request) -> Response:
    return Response.ok({"status": "ok"})

def home_handler(request: Request) -> Response:
    return Response.ok({"message": "Willkommen bei CloudMind"})

def echo_handler(request: Request) -> Response:
    return Response.ok(request.json) if request.json else Response.bad_request({"error": "Invalid JSON body"})

def db_post_handler(request: Request) -> Response:
    user_id = database.create_user(request.json['name'])
    return Response.created({"id": user_id})

def db_get_handler(request: Request) -> Response:
    if 'id' in request.path_params:
        user_id = request.path_params['id']
        user = database.get_user(user_id)
        return Response.ok(user) if user else Response.not_found({"error": "User not found"})
    users = database.list_users()
    return Response.ok(users) if users else Response.not_found({"error": "User not found"})

router.add("GET", "/health", health_handler)
router.add("GET", "/", home_handler)
router.add("POST", "/echo", echo_handler)
router.add("POST", "/users", db_post_handler)
router.add("GET", "/users", db_get_handler)
router.add("GET", "/users/{id}", db_get_handler)


def handle_connection(conn, addr):
  print(f"Connection from {addr}")
  try:
    request_data = conn.recv(1024).decode('utf-8')
    request = Request(request_data)
    response = router.dispatch(request)
    conn.sendall(response.to_bytes())
  except Exception as e:
    print(f"[ERROR]: {e}", file=sys.stderr)
    conn.sendall((Response.error(str(e))).to_bytes())
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