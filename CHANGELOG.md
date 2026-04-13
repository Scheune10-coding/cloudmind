# Changelog

All notable changes to CloudMind are documented here.

---

## [v0.1.0] — 2026-04-13

**Phase 1: Local Foundation (Weeks 1–6)**

The first complete milestone: a locally running AI chatbot built entirely from scratch — no web framework, no ORM. Every layer is hand-written and understood.

### Added

**Week 1 — HTTP Server from scratch**
- TCP socket server listening on port 8080
- Raw HTTP/1.1 request parsing (method, path, headers, body)
- Valid HTTP response generation with status codes
- Basic routing and error handling (404, 405, 500)

**Week 2 — Clean Architecture**
- `Request` and `Response` classes with full OOP design
- Dynamic `Router` with `{id}` path parameter support
- POST support with JSON body parsing
- CORS preflight handling (`OPTIONS *`)
- Unit tests for request, response, and router

**Week 3 — Database: Users, Sessions, Messages**
- SQLite schema with `users`, `sessions`, `messages`, and `summaries` tables
- Full CRUD via REST endpoints (`/users`, `/sessions`, `/sessions/{id}/messages`)
- Custom DB exception classes
- Unit tests for all database operations

**Week 4 — Configuration, Logging, and Automation**
- Centralized YAML config system (`config.yaml`) with `.env` overrides
- Structured logging with rotating file handler
- `start.sh` script: auto-creates venv, installs deps, initializes config on first run
- Message export script + cronjob wrapper
- `/stats` endpoint (user/session/message counts via pandas)
- Unit tests for config

**Week 5 — LLM Integration**
- `LLMClient` using OpenAI API via `requests` (no SDK)
- `/chat` endpoint — sends message, stores reply in DB
- Retry logic with exponential backoff for API errors
- `TokenTracker` for per-session token and cost tracking
- `/config` endpoint exposing active server configuration
- Unit tests for chat and token tracking

**Week 6 — Conversation Memory and HTML Client**
- Conversation history passed as context to the LLM
- `ContextManager`: auto-trims old messages when token budget is exceeded
- Automatic summarization of trimmed context (persisted in DB, survives restarts)
- Minimal HTML chat client served at `GET /` — no build step, single file
- Session management in the browser client (create user, create session, chat)

---

*Project started: 2026-03-22*
