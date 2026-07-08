# PROJECT_CONTEXT.md

# InterviewPilot

---

# Project Vision

InterviewPilot is a production-grade AI-powered interview preparation platform.

The objective is to build a startup-quality SaaS application rather than a college project.

The project is intended to become the flagship software engineering project for Software Engineering and AI/ML placements.

Every implementation should follow production software engineering practices.

---

# Current Project Version

v0.3.0

Date

08-07-2026

---

# Current Status

## Authentication Module

Status

✅ COMPLETED

Completed Features

- User Registration
- User Login
- PostgreSQL Integration
- SQLAlchemy ORM
- User Model
- Password Hashing (bcrypt)
- Password Verification
- Duplicate Username Validation
- Duplicate Email Validation
- JWT Authentication
- OAuth2 Password Flow
- JWT Token Generation
- JWT Verification
- Protected Routes
- Current User Endpoint (`GET /auth/me`)
- Swagger OAuth2 Authorization
- Database Transaction Rollback

Authentication has been completely implemented and tested.

---

# Current API Endpoints

GET /

GET /health

POST /auth/signup

POST /auth/login

GET /auth/me

All endpoints are fully functional.

---

# Current Backend Architecture

```
Browser

↓

Next.js Frontend

↓

REST API

↓

FastAPI

↓

Route Layer

↓

Schema Layer

↓

Service Layer

↓

Security Layer

↓

Database Layer

↓

PostgreSQL
```

---

# Current Folder Structure

```
backend/

app/

├── api/
│   ├── routes/
│   └── dependencies/
│
├── core/
│   └── security.py
│
├── db/
│   ├── database.py
│   └── init_db.py
│
├── models/
│   └── user.py
│
├── schemas/
│   └── auth.py
│
├── services/
│   └── auth.py
│
└── main.py
```

---

# Backend Design Rules

Every backend feature must follow this architecture.

```
Route

↓

Schema

↓

Service

↓

Security

↓

Database
```

Responsibilities

## Route

- Receive HTTP request
- Validate dependencies
- Call service
- Return response

No business logic.

---

## Schema

- Validate request
- Validate response

No business logic.

---

## Service

Contains all business logic.

Examples

- Signup
- Login
- Resume Upload
- Interview Generation

No HTTP handling.

---

## Security

Contains all authentication related utilities.

Examples

- Password Hashing
- Password Verification
- JWT Generation
- JWT Verification

No business logic.

---

## Database

Contains

- SQLAlchemy Models
- Database Sessions

---

# Current Database

Database

```
interviewpilot
```

Current Tables

```
users
```

Columns

- id
- username
- email
- hashed_password

---

# Current Tech Stack

Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

Backend

- FastAPI
- Python

Database

- PostgreSQL
- SQLAlchemy ORM

Authentication

- Passlib
- bcrypt
- python-jose
- OAuth2PasswordBearer
- python-multipart

Documentation

- Swagger/OpenAPI

---

# Development Workflow

Every feature must follow

```
Understand

↓

Design

↓

Implement

↓

Test

↓

Refactor

↓

Documentation

↓

Git Commit

↓

Git Push
```

A feature is NOT considered complete until all eight steps are finished.

---

# Coding Standards

Business logic belongs only inside Services.

Routes should remain thin.

Schemas should only validate data.

Security logic belongs inside `core/security.py`.

Models should only represent database tables.

Never duplicate business logic.

Always keep authentication reusable.

Follow production-level coding practices.

---

# Current Milestone

Authentication Module

Status

✅ COMPLETED

---

# Next Sprint

Sprint 5

Objective

Build the complete Frontend Authentication Module.

---

# Next Tasks

## Backend Cleanup

Before starting frontend, complete a short engineering cleanup.

Tasks

- Move password hashing utilities into `core/security.py`
- Remove unused imports
- Create response models for authentication
- Review authentication module for consistency
- Final cleanup before commit

Estimated Time

15–20 minutes

---

## Frontend Authentication

Build

- Signup Page
- Login Page
- Professional UI
- API Integration
- JWT Storage
- Logout
- Protected Routes
- Auto Login
- Authentication Context
- Redirect after Login

The frontend must use the existing authentication backend.

Do NOT rebuild backend authentication.

---

# Long-Term Roadmap

Phase 1 ✅

Foundation

Completed

---

Phase 2 ✅

Authentication

Completed

---

Phase 3

Resume Module

- Resume Upload
- Resume Parsing
- Skill Extraction

---

Phase 4

AI Interview

- Question Generator
- Company Specific Interviews
- Coding Interviews

---

Phase 5

AI Evaluation

- LLM Feedback
- Communication Analysis
- Technical Analysis

---

Phase 6

Dashboard

- Interview History
- Analytics
- Progress Tracking

---

Phase 7

DevOps

- Docker
- Docker Compose
- GitHub Actions
- CI/CD

---

Phase 8

Deployment

- Vercel
- Railway / Render
- Neon PostgreSQL

---

# AI Instructions

When continuing this project:

- Never rewrite completed modules unless fixing bugs.
- Build on top of the existing architecture.
- Follow the Route → Schema → Service → Security → Database architecture.
- Keep business logic inside services.
- Keep security logic inside `core/security.py`.
- Prefer production-grade implementations over tutorial-style code.
- Explain important architectural decisions before implementing them.
- Optimize for completing production-ready modules rather than isolated examples.

---

# End Goal

InterviewPilot should demonstrate

- Production Backend Engineering
- Frontend Engineering
- Authentication
- Database Design
- REST APIs
- AI Integration
- Docker
- CI/CD
- Cloud Deployment
- Software Architecture

The final product should resemble a real startup SaaS application rather than a college project.

This repository should be suitable for placement interviews and portfolio demonstrations.