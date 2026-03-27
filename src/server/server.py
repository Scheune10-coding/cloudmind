import socket
import threading
from src.server.request import Request
from src.server.response import Response
from src.server.router import Router
from src.db.database import Database
from src.server.controller.user import UserController
from src.server.controller.session import SessionController
from src.server.controller.message import MessageController
from src.db.exceptions import NotFoundError, ValidationError
from src.config.config import Config
from src.config.logging_setup import setup_logging
import time
import logging
logger = logging.getLogger(__name__)

# Router instanziieren und Routen registrieren
router = Router()
config = Config.load("config.yaml")
setup_logging(config.logging_level, config.logging_file)
database = Database(config.database_path)


user_controller = UserController(database)
session_controller = SessionController(database)
message_controller = MessageController(database)

def health_handler(request: Request) -> Response:
  return Response.ok({"status": "ok", "model": config.llm_model})

def home_handler(request: Request) -> Response:
  return Response.ok({"message": "Willkommen bei CloudMind"})

def echo_handler(request: Request) -> Response:
  return Response.ok(request.json) if request.json else Response.bad_request({"error": "Invalid JSON body"})

def stats_handler(request: Request) -> Response:
  stats = database.get_stats()
  return Response.ok(stats)

router.add("GET", "/health", health_handler)
router.add("GET", "/", home_handler)
router.add("POST", "/echo", echo_handler)
router.add("POST", "/users", user_controller.create)
router.add("GET", "/users", user_controller.list)
router.add("GET", "/users/{id}", user_controller.get)
router.add("POST", "/sessions", session_controller.create)
router.add("GET", "/users/{id}/sessions", session_controller.list)
router.add("GET", "/sessions/{id}", session_controller.get)
router.add("POST", "/sessions/{id}/messages", message_controller.create)
router.add("GET", "/sessions/{id}/messages", message_controller.list)
router.add("GET", "/stats", stats_handler)


def handle_connection(conn, addr):
  logger.info(f"Connection from {addr}") 
  start_time = time.time()
  try:
    request_data = conn.recv(1024).decode('utf-8')
  except Exception as e:
    logger.error(f"Error retrieving request data from {addr}")
    conn.close()
  try:
    request = Request(request_data) 
    response = router.dispatch(request)
    conn.sendall(response.to_bytes())
  except NotFoundError as e:
    conn.sendall((Response.not_found({"error": str(e)}).to_bytes()))
  except ValidationError as e:
    conn.sendall((Response.bad_request({"error": str(e)}).to_bytes()))
  except Exception as e:
    logger.error(f"Error handling request: {e}", exc_info=True)
    conn.sendall((Response.error({"error": str(e)}).to_bytes()))
  finally:
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.path} {response.status} {duration:.31}s")
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((config.host, config.port))
server.listen(5)
logger.info(f"Server is listening on port {config.port}...")

while True:
    conn = None
    try:
        conn, addr = server.accept()
        threading.Thread(target=handle_connection, args=(conn, addr)).start()
    except Exception as e:
        logger.error(f"Error accepting connection: {e}", exc_info=True)