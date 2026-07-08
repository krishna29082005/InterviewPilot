# Development Log

---

# Session 1

Date

2026-07-05

---

## Completed

- Created GitHub repository
- Created monorepo
- Installed Node.js
- Configured Next.js
- Configured TypeScript
- Configured TailwindCSS
- Configured ESLint
- Started development server
- Created first Git commit

---

## Decisions

- Next.js instead of Vite
- FastAPI instead of Flask
- Monorepo architecture
- TailwindCSS
- App Router

---

## Problems Faced

- Node PATH issue
- Nested repository issue
- README directory issue

---

## Learnings

- Git workflow
- Next.js initialization
- Professional repository setup

---

## Next Session

Initialize FastAPI backend

Create first API

Connect frontend and backend


---

# Session 2

**Date**

2026-07-06

---

## Objective

Initialize the FastAPI backend and establish the first frontend-backend communication.

---

## Completed

### Backend

- Created Python virtual environment
- Installed FastAPI
- Installed Uvicorn
- Generated `requirements.txt`
- Created scalable backend folder structure
- Created FastAPI application
- Added Root endpoint (`/`)
- Added Health endpoint (`/health`)
- Implemented modular routing using APIRouter
- Configured Swagger/OpenAPI documentation
- Configured CORS middleware

### Frontend

- Converted landing page into a Client Component
- Learned React `useState`
- Learned React `useEffect`
- Connected frontend to FastAPI backend using Fetch API
- Displayed live backend health status

### Git

- Created feature commit
- Updated `.gitignore`
- Removed virtual environment from Git tracking
- Created cleanup commit
- Pushed all changes to GitHub

---

## Decisions

- Use APIRouter for modular backend architecture
- Keep `main.py` minimal
- Separate routes by feature
- Use Fetch API for frontend-backend communication
- Configure CORS during development
- Never commit virtual environments to Git

---

## Problems Faced

### 1. Virtual Environment Tracking

Git started tracking the entire `.venv` directory.

**Solution**

- Updated `.gitignore`
- Removed `.venv` from Git index using:

```bash
git rm -r --cached backend/.venv
```

---

### 2. Frontend Could Not Reach Backend

Frontend displayed:

```
Backend Status: Offline
```

**Cause**

Browser blocked requests because of the Same-Origin Policy.

**Solution**

Configured FastAPI `CORSMiddleware`.

---

### 3. Git Confusion

Initially thought project changes had not been committed.

**Solution**

Verified commit history using:

```bash
git log --oneline
```

Confirmed everything had already been committed and pushed.

---

## Learnings

### FastAPI

- FastAPI project structure
- APIRouter
- OpenAPI
- Swagger Documentation

### React

- Client Components
- useState
- useEffect
- Fetch API
- Asynchronous requests

### Backend

- REST APIs
- JSON responses
- CORS
- HTTP communication

### Git

- .gitignore
- git rm --cached
- Professional commit workflow

---

## Architecture Achieved

```
Browser

↓

Next.js

↓

Fetch API

↓

FastAPI

↓

Python Logic

↓

JSON Response

↓

React State

↓

Updated UI
```

---

## Project Status

### Frontend

Landing Page
 
Backend Health Indicator

### Backend

FastAPI

APIRouter

Health Endpoint

 Swagger

### Integration
 Frontend connected to Backend

---
