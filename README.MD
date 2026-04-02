# CloudMind

CloudMind is a custom-built HTTP API server with integrated LLM capabilities (OpenAI). It manages users, chat sessions, and messages while providing token tracking with cost calculation. Built from scratch using raw TCP sockets without external web frameworks.

---
## Get Started

### 1. Clone GitHub-Repo

```bash
git clone https://github.com/Scheune10-coding/cloudmind.git
cd cloudmind
```

### 2. Start HTTP server

```bash
./start.sh
```

### Example requests

```bash
# 1) Get welcome message (GET /)
curl http://localhost:8080/

# 2) Check server health (GET /health)
curl http://localhost:8080/health

# 3) Echo JSON body (POST /echo)
curl -X POST http://localhost:8080/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'

# 4) Create a user (POST /users)
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# 5) Get all users (GET /users)
curl http://localhost:8080/users

# 6) Get specific user by ID (GET /users/{id})
curl http://localhost:8080/users/1

# 7) Create a session (POST /sessions)
curl -X POST http://localhost:8080/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "title": "Meine erste Session"}'

# 8) Get all sessions correlated to a specific user (GET /users/{id}/sessions)
curl http://localhost:8080/users/1/sessions

# 9) Get specific session by ID (GET /sessions/{id})
curl http://localhost:8080/sessions/1

# 10) Add a message to a session (POST /sessions/{id}/messages)
curl -X POST http://localhost:8080/sessions/1/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Hallo, CloudMind!"}'

# 11) Get all messages in a session (GET /sessions/{id}/messages)
curl http://localhost:8080/sessions/1/messages

# 12) Get db stats (GET /stats)
curl http://localhost:8080/stats

# 13) Send a message to the LLM (POST /chat)
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": 1, "message": "Was ist Cloud Computing?"}'

# 14) Get current config (GET /config)
curl http://localhost:8080/config

```

### Complete flow: User → Session → Messages → History

```bash
# Step 1: Create a user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Leon"}'
# → {"id": 1}

# Step 2: Create a session for that user
curl -X POST http://localhost:8080/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "title": "Erster Chat"}'
# → {"id": 1}

# Step 3: Add a message to the session
curl -X POST http://localhost:8080/sessions/1/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Hallo, CloudMind!"}'
# → {"id": 1}

# Step 4: Chat with the LLM
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": 1, "message": "Hallo, CloudMind!"}'
# → {"reply": "Hallo! Wie kann ich dir helfen?", "session_id": 1, "message_id": 2}

# Step 5: Read the conversation history
curl http://localhost:8080/sessions/1/messages
# → [{"id": 1, "role": "user", "content": "Hallo, CloudMind!", ...}, {"id": 2, "role": "assistant", "content": "Hallo! Wie kann ich dir helfen?", ...}]
```

---
## Project Structure

```
cloudmind/
├── scripts/
│   ├── export_messages.py   # Script for messages export
│   └── export.sh            # Cronjob script
│
├── src/
│   ├── config/
│   │   └── config.py        # Configuration class
│   │
│   ├── db/
│   │   ├── exceptions.py    # Exception classes
│   │   └── database.py      # Database class
│   │
│   ├── llm/
│   │   ├── exceptions.py    # Exception classes
│   │   ├── llm_client.py    # OpenAI API client with retry logic
│   │   └── token_tracker.py # Token usage and cost tracking
│   │
│   ├── logging/
│   │   └── logging_setup.py # Logging setup
│   │
│   └── server/
│       ├── controller/
│       │   ├── chat.py      # LLM chat controller
│       │   ├── message.py   # Message controller
│       │   ├── session.py   # Session controller
│       │   └── user.py      # User controller
│       │
│       ├── response.py      # HTTP response builder
│       ├── request.py       # HTTP request parser
│       ├── router.py        # Router with path parameters
│       └── server.py        # Main HTTP server
│
├── tests/                   # Unit tests (pytest)
├── data/                    # SQLite database (runtime)
├── logs/                    # Log files (runtime)
│
├── .env.example             # Example ENV
├── config.example.yaml      # Example YAML config
├── requirements.txt         # Python dependencies
├── start.sh                 # Start script
└── README.MD                # Project documentation
```

---
## Features

- Custom TCP socket server with HTTP/1.1 protocol support
- Dynamic route matching with path parameters (`{id}`)
- Request/response parsing (method, path, headers, body, query params)
- Controller pattern for route handlers
- SQLite database with users, sessions, and messages
- LLM integration (OpenAI API) with conversation history
- Token tracking with cost calculation (per-session and global)
- Retry logic with exponential backoff for API calls
- Configurable system prompt, model, temperature, and max tokens
- YAML + `.env` configuration system with environment variable overrides
- Structured logging with rotating file handler
- Error handling with proper HTTP status codes
- Unit tests with pytest
- Message export via cronjob

---
## How to use the server

Start the server (see Quick start above) and make requests to the endpoints listed below.

**Routes:**

| Route | Description | Status Code | Method |
|-------|-------------|-------------|--------|
| `/` | Main route - Welcome message | 200 | GET |
| `/health` | Health check endpoint and llm_model | 200 | GET |
| `/echo` | Echo endpoint - Returns JSON body | 200 | POST |
| `/users` | Create a new user (expects JSON with 'name') | 201 | POST |
| `/users` | Get a list of all users | 200 | GET |
| `/users/{id}` | Get a specific user by ID | 200 / 404 | GET |
| `/sessions` | Create a new session (expects JSON with 'user_id' and 'title') | 201 | POST |
| `/users/{id}/sessions` | Get a list of all sessions for a specific user | 200 | GET |
| `/sessions/{id}` | Get a specific session by ID | 200 / 404 | GET |
| `/sessions/{id}/messages` | Add a message to a session (expects JSON with 'content') | 201 | POST |
| `/sessions/{id}/messages` | Get all messages in a session (chronological) | 200 | GET |
| `/chat` | Send a message to the LLM (expects JSON with 'session_id' and 'message') | 200 | POST |
| `/stats` | Get database and token usage stats | 200 | GET |
| `/config` | Get current server configuration | 200 | GET |
| `/xyz` | All other routes - Not Found | 404 | * |

---
## Running Tests

> **Note:** Make sure your virtual environment is activated before running the tests so that `pytest` is available.
> ```bash
> source venv/bin/activate
> ```

### All tests

```bash
python3 -m pytest tests/ -v
```

### Single test module

```bash
python3 -m pytest tests/test_chat.py -v
```

Available test modules: `test_request`, `test_response`, `test_router`, `test_database`, `test_config`, `test_chat`, `test_token_tracker`

---
## Requirements

- Python 3.10+
- pytest >= 8.0.0
- pandas >= 1.0.0
- pyyaml
- requests
- python-dotenv

---
## License

This project is open source and available for educational purposes.