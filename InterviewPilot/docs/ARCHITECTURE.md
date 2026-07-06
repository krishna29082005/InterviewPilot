# InterviewPilot Architecture

## Overview

InterviewPilot is a production-grade AI-powered interview preparation platform built using a modern full-stack architecture.

The project follows a modular and scalable design so that new features (authentication, AI services, resume parsing, analytics, etc.) can be added without major architectural changes.

---

# Current Architecture

```
                    Browser
                       │
                       ▼
              Next.js Frontend
                 (React + TS)
                       │
                HTTP / REST API
                       │
                       ▼
              FastAPI Backend
                       │
                APIRouter Layer
                       │
                  Python Logic
```

---

# Current Tech Stack

## Frontend

- Next.js (App Router)
- React
- TypeScript
- Tailwind CSS

### Responsibilities

- User Interface
- API Calls
- State Management
- Dynamic Rendering

---

## Backend

- FastAPI
- Python
- APIRouter

### Responsibilities

- REST API
- Business Logic
- JSON Responses
- API Documentation (Swagger)

---

# Current Folder Structure

```
InterviewPilot/

├── frontend/
│   ├── src/
│   │   └── app/
│   │       └── page.tsx
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── health.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── docs/
├── docker/
├── scripts/
└── .github/
```

---

# Backend Architecture

```
                FastAPI Application
                        │
                        ▼
                app.include_router()
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
     Root Endpoint              Health Router
        "/"                      "/health"
```

The backend follows a modular routing architecture using **FastAPI APIRouter**.

Each feature will own its own router, making the application easier to maintain and extend.

Future routers will include:

- Authentication
- Resume
- Interview
- Dashboard
- AI

---

# Frontend Architecture

```
Browser

    │

    ▼

Next.js Page

    │

React Hooks

(useState + useEffect)

    │

Fetch API

    │

HTTP Request

    │

FastAPI

    │

JSON Response

    │

React State Update

    │

Updated UI
```

Current functionality:

- Landing Page
- Backend Health Check
- Dynamic Backend Status Indicator

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Welcome endpoint |
| GET | `/health` | Backend health status |

---

# CORS Configuration

The frontend and backend run on different origins during development.

Frontend

```
http://localhost:3000
```

Backend

```
http://127.0.0.1:8000
```

FastAPI uses **CORSMiddleware** to allow secure communication between the frontend and backend during development.

---

# Development Flow

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

# Architecture Principles

Current architecture follows:

- Modular Design
- Separation of Concerns
- Feature-based Routing
- RESTful APIs
- Scalable Folder Structure
- Production-ready Development Practices

---

# Planned Architecture

The following components will be added in future milestones:

## Authentication

- JWT Authentication
- Password Hashing
- Protected Routes
- Role-based Authorization

---

## Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations

---

## AI Pipeline

```
Resume

↓

Resume Parser

↓

Skill Extraction

↓

Question Generator

↓

Interview Session

↓

LLM Evaluation

↓

Feedback

↓

Dashboard
```

---

## Infrastructure

- Docker
- Docker Compose
- GitHub Actions
- CI/CD Pipeline

---

## Deployment

Frontend

↓

Vercel

Backend

↓

Railway / Render

Database

↓

Neon PostgreSQL

---

## Future Documentation

This document will later include:

- Authentication Flow
- Database ER Diagram
- Sequence Diagrams
- Deployment Diagram
- Docker Architecture
- AI System Design
- Caching Architecture
- Background Workers