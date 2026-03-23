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
## Project Structure

```
cloudmind/
├── src/
│   └── server/
│       ├── tcp_server.py    # Main HTTP server
│       ├── response.py      # HTTP response parser
│       └── request.py       # HTTP request parser
├── tests/
│   ├── test_response.py     # Unit tests for Response class
│   └── test_request.py      # Unit tests for Request class
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

### 1. Start the server

```bash
python3 src/server/tcp_server.py
```

### 2. Make request
```bash
curl http://localhost:8080<ROUTE>
```

**Routes:**

| Route | Description | Status Code |
|-------|-------------|-------------|
| `/` | Main route - Welcome message | 200 |
| `/health` | Health check endpoint | 200 |
| `/*` | All other routes - Not Found | 404 |

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

---

## Requirements

- Python 3.10+ (uses match/case syntax)
- pytest for running tests

---

## License

This project is open source and available for educational purposes.

