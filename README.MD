# CloudMind

CloudMind is a simple HTTP server that handles different routes and returns JSON responses. This project serves as a foundation for an extensible API server.

---
## Get Started

### 1. Clone GitHub-Repo

```bash
git clone https://github.com/Scheune10-coding/cloudmind.git
cd cloudmind
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip3 install -r requirements.txt
```

---
## Quick start

Start the server and try example requests immediately.

### Start the server

```bash
python3 src/server/server.py
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

# Step 4: Read the conversation history
curl http://localhost:8080/sessions/1/messages
# → [{"id": 1, "session_id": 1, "role": "user", "content": "Hallo, CloudMind!", "created_at": "..."}]
```

---
## Project Structure

```
cloudmind/
├── src/
│   ├── config/
│   │   ├── config.py        # Configuration class
│   │   └── logging_setup.py # Logging setup
│   │
│   ├── db/
│   │   ├── exceptions.py    # Exception classes
│   │   └── database.py      # Database class
│   │  
│   └── server/
│       ├── controller/
│       │   ├── message.py   # Message controller
│       │   ├── session.py   # Session controller
│       │   └── user.py      # User controller
│       │ 
│       ├── response.py      # HTTP response parser
│       ├── request.py       # HTTP request parser
│       ├── router.py        # Router-class
│       └── server.py        # Main HTTP server
│ 
├── tests/
│   ├── test_config.py       # Unit tests for configuration system
│   ├── test_database.py     # Unit tests for database operations
│   ├── test_response.py     # Unit tests for Response class
│   ├── test_request.py      # Unit tests for Request class
│   └── test_router.py       # Unit tests for Router class
│
├── config.example.xaml      # Example YAML
├── .env.example             # Example ENV
├── requirements.txt         # Python dependencies
└── README.MD                # Project documentation
```

---
## Features

- Custom TCP socket server
- HTTP/1.1 protocol support
- JSON response handling
- Dynamic route matching with path parameters ({id})
- Request and response parsing (method, path, headers, body, query params)
- Error handling with proper status codes
- Unit tests with pytest
- SQLite database integration
- Controller pattern for route handlers

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
| `/stats` | Get db stats | 200 | GET |
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

### Request-Class tests

```bash
python3 -m pytest tests/test_request.py -v
```

### Response-Class tests

```bash
python3 -m pytest tests/test_response.py -v
```

### Router-Class tests

```bash
python3 -m pytest tests/test_router.py -v
```

### Database operations tests

```bash
python3 -m pytest tests/test_database.py -v
```

### Configuration system tests

```bash
python3 -m pytest tests/test_config.py -v
```

---
## Requirements

- Python 3.10+
- pytest for running tests

---
## License

This project is open source and available for educational purposes.