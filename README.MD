# CloudMind

A custom HTTP API server with integrated LLM capabilities, built from scratch using raw TCP sockets — no external web frameworks. Manages users, chat sessions, and messages with token tracking, cost calculation, and automatic context window management.

## Tech Stack

- **Language:** Python 3.10+
- **Server:** Custom TCP socket server (HTTP/1.1, no framework)
- **Database:** SQLite (via `sqlite3`)
- **LLM:** OpenAI API (gpt-4o, configurable)
- **Config:** YAML + `.env` with environment variable overrides
- **Analytics:** pandas (used for message statistics in `/stats`)
- **Testing:** pytest

## Prerequisites

- Python 3.10+
- An OpenAI API key

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/Scheune10-coding/cloudmind.git
cd cloudmind

# 2. Start the server (handles venv, deps, config, and directories automatically)
./start.sh
```

On first run, `start.sh` will copy `config.example.yaml` to `config.yaml`, `.env.example` to `.env` and exit — edit `config.yaml` to adjust the model, system prompt, etc., insert your API-key to `.env` and then run `./start.sh` again.

## Configuration

`config.yaml` controls all server behavior. Environment variables in `.env` take precedence.

```yaml
server:
  host: "localhost"
  port: 8080

database:
  path: "data/cloudmind.db"

logging:
  level: "INFO"
  file: "logs/cloudmind.log"

llm:
  model: "gpt-4o"
  max_tokens: 1000
  temperature: 0.7
  system_prompt: "You are a helpful assistant."
```

Any `config.yaml` value can be overridden via environment variables in `.env`:

```
# Required
LLM_API_KEY=sk-your-api-key-here

# Optional overrides
SERVER_HOST=localhost
SERVER_PORT=8080
DATABASE_PATH=data/cloudmind.db
LOGGING_LEVEL=INFO
LOGGING_FILE=logs/cloudmind.log
LLM_MODEL_NAME=gpt-4o
LLM_MAX_TOKENS=1000
LLM_CONTEXT_MAX_TOKENS=4000
LLM_TEMPERATURE=0.7
LLM_SYSTEM_PROMPT=You are a helpful assistant.
```

## API Reference

| Method | Route | Description | Status |
|--------|-------|-------------|--------|
| GET | `/` | Web UI (serves `static/index.html`) | 200 |
| GET | `/health` | Health check + active model | 200 |
| POST | `/echo` | Echo JSON body | 200 |
| POST | `/users` | Create user `{"name": "..."}` | 201 |
| GET | `/users` | List all users | 200 |
| GET | `/users/{id}` | Get user by ID | 200 / 404 |
| POST | `/sessions` | Create session `{"user_id": 1, "title": "..."}` | 201 |
| GET | `/users/{id}/sessions` | List sessions for a user | 200 |
| GET | `/sessions/{id}` | Get session by ID | 200 / 404 |
| POST | `/sessions/{id}/messages` | Add message `{"content": "..."}` | 201 |
| GET | `/sessions/{id}/messages` | Get all messages (chronological) | 200 |
| POST | `/chat` | Chat with LLM `{"session_id": 1, "message": "..."}` | 200 |
| GET | `/stats` | DB and token usage stats (users, sessions, messages, per-role counts, timestamps) | 200 |
| GET | `/config` | Current server configuration | 200 |
| OPTIONS | `*` | CORS preflight — responds with allowed methods and headers | 200 |

## Example Flow

```bash
# Create a user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Leon"}'
# → {"id": 1}

# Create a session
curl -X POST http://localhost:8080/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "title": "First Chat"}'
# → {"id": 1}

# Chat with the LLM
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": 1, "message": "What is cloud computing?"}'
# → {"reply": "...", "session_id": 1, "message_id": 2}

# Read conversation history
curl http://localhost:8080/sessions/1/messages
```

## Architecture

```
cloudmind/
├── scripts/
│   ├── export_messages.py     # Message export script
│   └── export.sh              # Cronjob wrapper
│
├── src/
│   ├── config/
│   │   └── config.py          # Singleton config (YAML + env)
│   │
│   ├── db/
│   │   ├── database.py        # SQLite database layer (users, sessions, messages, summaries)
│   │   └── exceptions.py      # DB exception types
│   │
│   ├── llm/
│   │   ├── llm_client.py      # OpenAI API client (retry + backoff)
│   │   ├── token_tracker.py   # Token usage and cost tracking
│   │   ├── context_manager.py # Context trimming and summarization
│   │   └── exceptions.py      # LLM exception types
│   │
│   ├── logging/
│   │   └── logging_setup.py   # Rotating file handler setup
│   │
│   └── server/
│       ├── server.py          # TCP socket server (main loop, routing, DI)
│       ├── request.py         # HTTP request parser
│       ├── response.py        # HTTP response builder (JSON + HTML, CORS headers)
│       ├── router.py          # Dynamic route matching with {id} params + OPTIONS handling
│       └── controller/
│           ├── chat.py        # LLM chat handler
│           ├── message.py     # Message CRUD
│           ├── session.py     # Session CRUD
│           └── user.py        # User CRUD
│
├── static/
│   └── index.html             # Web UI (chat interface served at GET /)
│
├── tests/                     # pytest unit tests
├── data/                      # SQLite database (runtime, git-ignored)
├── logs/                      # Log files (runtime, git-ignored)
├── .env.example               # Environment variable template
├── config.example.yaml        # Config template
├── requirements.txt           # Python dependencies
└── start.sh                   # Server start script
```

### Web UI

A minimal chat interface is served at `GET /`. It talks directly to the API (`/users`, `/sessions`, `/chat`) via `fetch` in the browser. No build step required — it's a single self-contained HTML file.

### Context Window Management

When a session's conversation history grows too large, the context manager automatically:

1. **Trims** old messages from the front, keeping recent history within the token budget
2. **Summarizes** trimmed context using the LLM and injects the summary as a system message

The summary is persisted in the `sessions.summary` column so it survives server restarts.

This prevents token overflow without losing conversational continuity.

## Running Tests

```bash
# Activate virtual environment first
source venv/bin/activate

# Run all tests
python3 -m pytest tests/ -v

# Run a specific module
python3 -m pytest tests/test_chat.py -v
```

Available test modules: `test_request`, `test_response`, `test_router`, `test_database`, `test_config`, `test_chat`, `test_token_tracker`

## License

Open source — available for educational purposes.
