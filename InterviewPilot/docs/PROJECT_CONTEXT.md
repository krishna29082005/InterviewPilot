# InterviewPilot

---

# Project Vision

InterviewPilot is a production-grade AI-powered interview preparation platform.

The goal is to build a startup-quality SaaS application that demonstrates strong backend engineering, frontend engineering, AI integration, and practical product thinking.

The repository is intended to be suitable for placement interviews, portfolio demonstrations, and long-term expansion into interview practice and analytics.

---

# Current Project Version

v0.7.0

Date

23-08-2026
`
---

# Current Status

## Authentication Module

Status

âœ… COMPLETED

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

âœ… COMPLETED

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

âœ… COMPLETED

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

âœ… COMPLETED

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

## Recommended Roles / Career Fit

Status

âœ… COMPLETED

Completed Features

- ATS-driven role recommendations
- Gemini role recommendation extraction
- Deterministic fallback role detection
- Career Fit / Recommended Roles UI

---

## Job Description Matching

Status

âœ… COMPLETED

Completed Features

- Job description input and analysis
- Gemini requirement extraction
- Fallback job requirement parsing
- Deterministic resume/job matching
- JobMatchAnalysis output

---

## Job Match Frontend

Status

âœ… COMPLETED

Completed Features

- Job Match page
- Authenticated access
- Analyze and clear actions
- Match score display
- Matching and missing skills
- Matching and missing keywords
- Strengths, gaps, and recommendations
- Sidebar navigation entry

---

## Frontend Dashboard

Status

âœ… COMPLETED

Completed Features

- Resume dashboard
- ATS dashboard
- Job Match page
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
- `POST /job-match/analyze`

---

# Current Backend Architecture

```
Browser
   â†“
Next.js Frontend
   â†“
REST API
   â†“
FastAPI
   â†“
Route Layer
   â†“
Service Layer
   â†“
AI ProviderFactory
   â†“
Gemini Provider
   â†“
Fallback Parser / Fallback ATS / Fallback Job Match
   â†“
Pydantic Schemas
   â†“
Local Storage
```

---

# Current Folder Structure

```
backend/
â””â”€â”€ app/
    â”œâ”€â”€ api/
    â”‚   â”œâ”€â”€ dependencies/
    â”‚   â””â”€â”€ routes/
    â”œâ”€â”€ ai/
    â”‚   â”œâ”€â”€ parsers/
    â”‚   â”œâ”€â”€ prompts/
    â”‚   â”œâ”€â”€ providers/
    â”‚   â”œâ”€â”€ schemas/
    â”‚   â””â”€â”€ services/
    â”œâ”€â”€ core/
    â”œâ”€â”€ db/
    â”œâ”€â”€ models/
    â”œâ”€â”€ schemas/
    â””â”€â”€ services/

frontend/
â””â”€â”€ src/
    â”œâ”€â”€ app/
    â”œâ”€â”€ components/
    â”œâ”€â”€ context/
    â”œâ”€â”€ hooks/
    â”œâ”€â”€ lib/
    â””â”€â”€ types/
```

---

# Backend Design Rules

Every backend feature follows this pattern:

```
Route
â†“
Schema
â†“
Service
â†“
Provider / Parser
â†“
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
- Job description matching orchestration

## Provider / Parser

- Gemini provider
- Resume fallback parser
- ATS fallback logic
- Job match fallback parser

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
â†“
Extract Text
â†“
Clean Text
â†“
Gemini Resume Parser
â†“
ResumeSchema
â†“
Save Analysis JSON
```

## ATS Pipeline

```
ResumeSchema
â†“
Gemini ATS Analysis
â†“
ATSAnalysis
```

## Recommended Roles / Career Fit Pipeline

```
ResumeSchema
â†“
ATS Service
â†“
Gemini role recommendation
OR
Fallback role detection
â†“
RecommendedRole[]
â†“
Career Fit UI
```

## Job Match Pipeline

```
Job Description
â†“
Gemini requirement extraction
â†“
JobRequirements
â†“
Deterministic matching
â†“
JobMatchAnalysis
â†“
Frontend
```

## Fallback Strategy

If Gemini is unavailable, returns invalid JSON, or is rate limited, the app falls back to deterministic local logic instead of crashing.

This keeps the resume, ATS, role recommendation, and job matching flows usable even under load.

---

# Roadmap Status

## Completed

- Authentication
- Resume Upload
- Resume Parsing
- Fallback Resume Parser
- ATS Analysis
- Fallback ATS
- Recommended Roles / Career Fit
- Job Description Matching
- Job Match Frontend
- Resume Dashboard
- ATS Dashboard

## Planned

- Mock Interview
- AI Interview Evaluator
- Analytics Dashboard

---

# Notes for Future Work

- Keep business logic inside services.
- Keep AI provider-specific logic behind the provider layer.
- Prefer deterministic fallback behavior when Gemini is unavailable.
- Do not change the frontend contract unless the API changes intentionally.
- Mock Interview is the next major feature.
