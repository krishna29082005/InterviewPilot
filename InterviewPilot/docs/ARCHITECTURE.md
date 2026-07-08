# InterviewPilot Architecture

## Overview

InterviewPilot is a production-grade AI-powered interview preparation platform built using a modern full-stack architecture.

The project follows a modular, layered, and scalable architecture where every component has a single responsibility. This makes the codebase maintainable, testable, and easy to extend as new features such as AI interview generation, resume parsing, analytics, and dashboards are added.

---

# Current High-Level Architecture

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
                  APIRouter
                       │
                    Schemas
                  (Pydantic)
                       │
                  Service Layer
               (Business Logic)
                       │
                 SQLAlchemy ORM
                       │
                       ▼
                  PostgreSQL
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
- Authentication UI

---

## Backend

- FastAPI
- Python
- APIRouter
- Pydantic

### Responsibilities

- REST API
- Request Validation
- Business Logic
- Authentication
- JSON Responses
- API Documentation (Swagger)

---

## Database

- PostgreSQL
- SQLAlchemy ORM

### Responsibilities

- Persistent Data Storage
- User Management
- Authentication Data
- Future Resume & Interview Data

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
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── health.py
│   │       └── auth.py
│   │
│   ├── schemas/
│   │   └── auth.py
│   │
│   ├── services/
│   │   └── auth.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── init_db.py
│   │
│   └── main.py
│
│   requirements.txt
│
├── docs/
├── docker/
├── scripts/
└── .github/
```

---

# Backend Architecture

```
                 HTTP Request
                       │
                       ▼
                  FastAPI Route
                       │
                       ▼
             Pydantic Schema Validation
                       │
                       ▼
                Service Layer
             (Business Logic)
                       │
                       ▼
               SQLAlchemy ORM
                       │
                       ▼
                 PostgreSQL
                       │
                       ▼
                JSON Response
```

---

## Backend Components

### Route Layer

Responsibilities

- Receives HTTP requests
- Calls the correct service
- Returns API responses
- Injects database session

Current Routes

- Health
- Authentication

---

### Schema Layer

Responsibilities

- Validate request data
- Validate response data
- Prevent invalid input
- Type safety

Current Schemas

- User Signup

---

### Service Layer

Responsibilities

- Business Logic
- Password Hashing
- Duplicate User Validation
- Database Transactions

Current Services

- User Signup

---

### Database Layer

Responsibilities

- Database Session
- ORM Models
- CRUD Operations
- Transactions

Current Models

- User

---

# Authentication Flow

Current Signup Flow

```
Client

↓

POST /auth/signup

↓

Route

↓

Pydantic Validation

↓

Check Username

↓

Check Email

↓

Hash Password (bcrypt)

↓

SQLAlchemy

↓

PostgreSQL

↓

Success Response
```

---

# Frontend Architecture

```
Browser

↓

Next.js

↓

React Components

↓

useEffect / useState

↓

Fetch API

↓

FastAPI

↓

JSON Response

↓

React State Update

↓

Updated UI
```

Current Functionality

- Landing Page
- Backend Health Check
- Dynamic Backend Status
- API Integration

---

# Current API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/` | Welcome Endpoint |
| GET | `/health` | Backend Health Status |
| POST | `/auth/signup` | Register New User |

---

# Database Design

Current Tables

```
users

id
username
email
hashed_password
```

Current Features

- Unique Username
- Unique Email
- Password Hashing
- Duplicate Validation
- Transaction Rollback

---

# Development Flow

```
Browser

↓

Next.js

↓

REST API

↓

FastAPI

↓

Route

↓

Schema

↓

Service

↓

SQLAlchemy

↓

PostgreSQL

↓

JSON Response

↓

Frontend Update
```

---

# Architecture Principles

Current architecture follows

- Layered Architecture
- Separation of Concerns
- Feature-based Routing
- Modular Design
- RESTful APIs
- ORM Pattern
- Production-ready Development Practices
- Scalable Folder Structure

---

# Planned Architecture

## Authentication

- Login API
- JWT Authentication
- Protected Routes
- Refresh Tokens
- Role-based Authorization

---

## Database

- Alembic Migrations
- Database Relationships
- Index Optimization
- Soft Deletes

---

## Resume Module

- Resume Upload
- Resume Storage
- Resume Parsing
- Skill Extraction

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

# Future Documentation

This document will later include

- JWT Authentication Flow
- Database ER Diagram
- Sequence Diagrams
- Deployment Diagram
- Docker Architecture
- AI System Design
- Caching Strategy
- Background Workers
- Monitoring & Logging