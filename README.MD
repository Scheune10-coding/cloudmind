# CloudMind

CloudMind is a simple HTTP server that handles different routes and returns JSON responses. This project serves as a foundation for an extensible API server.

---
## How to use the server

### 1. Clone GitHub-Repo

```
git clone https://github.com/Scheune10-coding/cloudmind.git
```

### 2. Start the server

```
python3 src/server/tcp_server.py
```

### 3. Make request
```
curl http://localhost:8080<ROUTE>
```

**Routes:**

| Route | Description | Status Code |
|-------|-------------|-------------|
| `/` | Main route - Welcome message | 200 |
| `/health` | Health check endpoint | 200 |
| `/*` | All other routes - Not Found | 404 |
