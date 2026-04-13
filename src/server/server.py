import logging
import socket
import threading
import time

from src.config.config import Config
from src.db.database import Database
from src.db.exceptions import NotFoundError, ValidationError
from src.llm.llm_client import LLMClient
from src.logging.logging_setup import setup_logging
from src.server.controller.chat import ChatController
from src.server.controller.message import MessageController
from src.server.controller.session import SessionController
from src.server.controller.user import UserController
from src.server.request import Request
from src.server.response import Response
from src.server.router import Router
from src.llm.token_tracker import TokenTracker

logger = logging.getLogger(__name__)

RECV_BUFFER_SIZE = 65536
LISTEN_BACKLOG = 5

router = Router()
config = Config.load("config.yaml")
setup_logging(config.logging_level, config.logging_file)
database = Database(config.database_path)
token_tracker = TokenTracker()
llm_client = LLMClient(token_tracker)

user_controller = UserController(database)
session_controller = SessionController(database)
message_controller = MessageController(database)
chat_controller = ChatController(database, llm_client)


def health_handler(request: Request) -> Response:
  return Response.ok({"status": "ok", "model": config.llm_model})


def home_handler(request: Request) -> Response:
  with open('static/index.html', 'r', encoding='utf-8') as f:
    return Response.html(f.read())


def echo_handler(request: Request) -> Response:
  if request.json:
    return Response.ok(request.json)
  return Response.bad_request({"error": "Invalid JSON body"})


def stats_handler(request: Request) -> Response:
  stats = database.get_stats()
  stats["token_usage"] = {
    "total_prompt": token_tracker.total_prompt,
    "total_completion": token_tracker.total_completion,
    "total_cost": token_tracker.get_cost()
  }
  return Response.ok(stats)


def config_handler(request: Request) -> Response:
  return Response.ok(config.to_dict())


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
router.add("POST", "/chat", chat_controller.create)
router.add("GET", "/config", config_handler)


def handle_connection(conn, addr):
  logger.info("Connection from %s", addr)
  start_time = time.time()
  request = None
  response = None
  try:
    request_data = conn.recv(RECV_BUFFER_SIZE).decode("utf-8")
  except Exception:
    logger.error("Error retrieving request data from %s", addr)
    conn.close()
    return
  try:
    request = Request(request_data)
    response = router.dispatch(request)
    conn.sendall(response.to_bytes())
  except NotFoundError as e:
    conn.sendall(Response.not_found({"error": str(e)}).to_bytes())
  except ValidationError as e:
    conn.sendall(Response.bad_request({"error": str(e)}).to_bytes())
  except Exception as e:
    logger.error("Error handling request: %s", e, exc_info=True)
    conn.sendall(Response.error(str(e)).to_bytes())
  finally:
    duration = time.time() - start_time
    method = request.method if request else "UNKNOWN"
    path = request.path if request else "UNKNOWN"
    status = response.status if response else 500
    logger.info("%s %s %s %.3fs", method, path, status, duration)
    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((config.host, config.port))
server.listen(LISTEN_BACKLOG)
logger.info("Server is listening on port %d...", config.port)

while True:
  conn = None
  try:
    conn, addr = server.accept()
    threading.Thread(target=handle_connection, args=(conn, addr)).start()
  except Exception as e:
    logger.error("Error accepting connection: %s", e, exc_info=True)
