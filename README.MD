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
# (or python3 src/server/tcp_server.py for the deprecated single-threaded example)
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
```

---
## Project Structure

```
cloudmind/
├── src/
│   └── server/
│       ├── tcp_server.py    # HTTP server (DEPRECATED)
│       ├── response.py      # HTTP response parser
│       ├── request.py       # HTTP request parser
│       ├── router.py        # Router-class
│       └── server.py        # Main HTTP server
│ 
├── tests/
│   ├── test_response.py     # Unit tests for Response class
│   ├── test_request.py      # Unit tests for Request class
│   └── test_router.py       # Unit tests for Router class
│ 
├── requirements.txt         # Python dependencies
└── README.MD                # Project documentation
```

---
## Features

- Custom TCP socket server
- HTTP/1.1 protocol support
- JSON response handling
- Route matching with pattern matching
- Request and response parsing (method, path, headers, body, query params)
- Error handling with proper status codes
- Unit tests with pytest

---
## How to use the server

Start the server (see Quick start above) and make requests to the endpoints listed below.

**Routes:**

| Route | Description | Status Code | Method |
|-------|-------------|-------------|--------|
| `/` | Main route - Welcome message | 200 | GET |
| `/health` | Health check endpoint | 200 | GET |
| `/echo` | Echo endpoint - Returns JSON body | 200 | POST |
| `/*` | All other routes - Not Found | 404 | * |

---
## Running Tests

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

---
## Requirements

- Python 3.10+ (uses match/case syntax)
- pytest for running tests

---
## License

This project is open source and available for educational purposes.

