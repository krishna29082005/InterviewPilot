# InterviewPilot

---

# Project Vision

InterviewPilot is a production-grade AI-powered interview preparation platform.

The goal is to build a startup-quality SaaS application that demonstrates strong backend engineering, frontend engineering, AI integration, and practical product thinking.

The repository is intended to be suitable for placement interviews, portfolio demonstrations, and long-term expansion into interview practice and analytics.

---

# Current Project Version

v0.6.0

Date

07-08-2026

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
- Password Hashing
- Password Verification
- Duplicate Username Validation
- Duplicate Email Validation
- JWT Authentication
- OAuth2 Password Flow
- JWT Token Generation
- JWT Verification
- Protected Routes
- Current User Endpoint (`GET /auth/me`)
- Database Transaction Rollback

---

## Resume Module

Status

✅ COMPLETED

Completed Features

- Resume Upload
- Resume Download
- Resume Delete
- Resume Information API
- Resume Dashboard
- Local resume storage

---

## Resume Parsing

Status

✅ COMPLETED

Completed Features

- PDF text extraction using PyMuPDF
- Text cleaning
- Gemini resume parser
- Deterministic fallback parser
- ResumeSchema validation
- Hyperlink extraction from PDF annotations
- Resume regeneration when analysis is missing

---

## ATS Analysis

Status

✅ COMPLETED

Completed Features

- Gemini ATS analysis
- ATS score
- Summary
- Strengths
- Weaknesses
- Missing keywords
- Formatting issues
- Recommendations
- Fallback ATS analysis

---

## Frontend Dashboard

Status

✅ COMPLETED

Completed Features

- Resume dashboard
- ATS dashboard
- Structured resume analysis layout
- Better link rendering
- Protected dashboard experience

---

# Current API Endpoints

- `GET /`
- `GET /health`
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`
- `POST /resume/upload`
- `GET /resume/info`
- `GET /resume/download`
- `DELETE /resume/delete`
- `GET /ats/analysis`

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
Service Layer
   ↓
AI ProviderFactory
   ↓
Gemini Provider
   ↓
Fallback Parser / Fallback ATS
   ↓
Pydantic Schemas
   ↓
Local Storage
```

---

# Current Folder Structure

```
backend/
└── app/
    ├── api/
    │   ├── dependencies/
    │   └── routes/
    ├── ai/
    │   ├── parsers/
    │   ├── prompts/
    │   ├── providers/
    │   ├── schemas/
    │   └── services/
    ├── core/
    ├── db/
    ├── models/
    ├── schemas/
    └── services/

frontend/
└── src/
    ├── app/
    ├── components/
    ├── context/
    ├── hooks/
    ├── lib/
    └── types/
```

---

# Backend Design Rules

Every backend feature follows this pattern:

```
Route
↓
Schema
↓
Service
↓
Provider / Parser
↓
Storage
```

Responsibilities

## Route

- Receive HTTP request
- Validate dependencies
- Call service
- Return response

## Schema

- Validate request data
- Validate response data

## Service

- Resume upload orchestration
- ATS generation orchestration
- Gemini-first execution
- Fallback handling

## Provider / Parser

- Gemini provider
- Resume fallback parser
- ATS fallback logic

## Storage

- Uploaded resume PDFs
- Parsed resume analysis JSON

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
- Uvicorn
- Pydantic
- JWT
- Passlib
- PyMuPDF
- Google Gemini

Storage

- Local filesystem

---

# AI Workflow

## Resume Pipeline

```
Resume Upload
↓
Extract Text
↓
Clean Text
↓
Gemini Resume Parser
↓
ResumeSchema
↓
Save Analysis JSON
```

## ATS Pipeline

```
ResumeSchema
↓
Gemini ATS Analysis
↓
ATSAnalysis
```

## Fallback Strategy

If Gemini is unavailable, returns invalid JSON, or is rate limited, the app falls back to deterministic local logic instead of crashing.

This keeps the resume and ATS dashboards usable even under load.

---

# Roadmap Status

## Completed

- Authentication
- Resume Upload
- Resume Parsing
- Fallback Resume Parser
- ATS Analysis
- Fallback ATS
- Resume Dashboard
- ATS Dashboard

## Planned

- Job Description Matching
- Mock Interview
- AI Interview Evaluator
- Analytics Dashboard

---

# Notes for Future Work

- Keep business logic inside services.
- Keep AI provider-specific logic behind the provider layer.
- Prefer deterministic fallback behavior when Gemini is unavailable.
- Do not change the frontend contract unless the API changes intentionally.

