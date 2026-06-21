# Standalone Auth Service

This is a backend development project with purpose of learning. I tried to build an authentication app that's functional in a wide range of applications and services across many sectors. I faced many new backend and software development processes as I went deeper — concepts like authentication, rate limiting, JWT, token design, database design for different use cases, and FastAPI usage. I came to understand the server side and client side requests, and how information is served, covering the project with structured logging in order to make data and actions observable throughout the app. Set the server on a VPS on Oracle Cloud with free usage — learned basic concepts of software operations. This project was intended to be made under the plan of creating engineering culture and experience, with a lot to come in the near future: operations and services that are scalable, maintainable, and self-reliant.

---

## What It Does

This service handles the full authentication lifecycle for a user:

- **Register** a new account (bcrypt password hashing)
- **Login** — issues a short-lived JWT access token and a long-lived refresh token; captures IP address and user-agent for session tracking
- **Refresh** — swap a valid refresh token for a new access token
- **Revoke** — invalidate a single refresh token
- **Revoke all** — invalidate every active refresh token for a user (useful for "sign out everywhere")
- **Logout** — blacklist the current access token so it can't be reused before expiry
- **Session management** — list all active sessions and delete individual ones

Rate limiting is applied on the login endpoint: 5 requests per IP per 5-minute window.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Create a new user |
| POST | `/auth/login` | Login, get access + refresh token |
| POST | `/auth/refresh` | Get a new access token |
| POST | `/auth/revoke` | Revoke a refresh token |
| POST | `/auth/revoke-all` | Revoke all tokens for the user |
| POST | `/auth/logout` | Blacklist the current access token |
| GET | `/auth/me` | Get current user info |
| GET | `/auth/sessions` | List active sessions |
| DELETE | `/auth/sessions/{id}` | Delete a specific session |

## Tech Stack

- **FastAPI** — HTTP framework and routing
- **PostgreSQL** — persistent storage for users, tokens, sessions, blacklist
- **SQLAlchemy 2.0** — ORM and database interaction layer
- **Alembic** — schema migrations
- **python-jose** — JWT encoding/decoding
- **passlib/bcrypt** — password hashing
- **structlog** — structured JSON logging throughout the application
- **pytest** — testing

## Project Structure

```
auth-service/
├── app/
│   ├── api/
│   │   └── auth.py          # Route definitions
│   ├── core/
│   │   ├── config.py        # Settings from environment
│   │   └── security.py      # JWT, password hashing, rate limiter
│   ├── db/
│   │   └── database.py      # SQLAlchemy engine and session
│   ├── models/              # ORM models: User, RefreshToken, Session, Blacklist
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/
│   │   └── auth.py          # Business logic layer
│   ├── logger.py            # structlog configuration
│   └── main.py              # FastAPI app, middleware, router registration
├── alembic/                 # Migration scripts
├── tests/
└── requirements.txt
```

## Running Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (copy and fill in .env)
cp .env.example .env

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## What I Learned

Going through this project, I worked with:

- The difference between access tokens and refresh tokens — why they exist separately, what each one protects against
- How token revocation works and why it's non-trivial with JWTs (stateless tokens require a blacklist for early invalidation)
- How session tracking (IP + user-agent) gives users visibility into where they're logged in
- In-memory rate limiting and its limitations vs. a distributed store
- How the service, schema, model, and route layers each have distinct responsibilities — and what breaks when they blur
- Running and managing a service on a VPS (Oracle Cloud Free Tier)
- Structured logging as a practice for making server-side behavior observable

## Limitations

This is a learning project, not production-ready. Known limitations:

- Rate limiter is in-memory — resets on restart, doesn't work across multiple processes
- No HTTPS enforcement at the application level (handled externally)
- CORS is open (`allow_origins=["*"]`) — set for development convenience
- No token rotation on refresh (same refresh token stays valid until explicit revocation)
