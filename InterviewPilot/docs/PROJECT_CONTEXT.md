# InterviewPilot

---

# Project Vision

InterviewPilot is a production-grade AI-powered interview preparation platform.

The goal is to build a startup-quality SaaS application that demonstrates strong backend engineering, frontend engineering, AI integration, and practical product thinking.

The repository is intended to be suitable for placement interviews, portfolio demonstrations, and long-term expansion into interview practice, personalized career guidance, and analytics.

---

# Current Project Version

v0.8.0

Date

01-09-2026

---

# Current Status

## Authentication Module

Status

✅ COMPLETED

Completed Features

- User Registration
- User Login
- PostgreSQL Integration
- SQLAlchemy ORMgit status

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
- One-resume-per-user handling
- Resume overwrite handling

---

## Resume Parsing

Status

✅ COMPLETED

Completed Features

- PDF text extraction using PyMuPDF
- Text cleaning
- Gemini resume parser
- ResumeSchema validation
- Deterministic fallback parser
- Hyperlink extraction from PDF annotations
- Resume regeneration when analysis is missing
- Resume analysis persistence

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
- ATS analysis persistence
- Cached ATS analysis retrieval

---

## Recommended Roles / Career Fit

Status

✅ COMPLETED

Completed Features

- ATS-driven role recommendations
- Gemini role recommendation extraction
- Deterministic fallback role detection
- Career Fit / Recommended Roles UI

---

## Job Description Matching

Status

✅ COMPLETED

Completed Features

- Job description input and analysis
- Gemini requirement extraction
- Fallback job requirement parsing
- Deterministic resume/job matching
- JobMatchAnalysis output
- Latest Job Match result persistence
- Job description persistence with Job Match result

---

## Job Match Frontend

Status

✅ COMPLETED

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

## Mock Interview

Status

✅ COMPLETED

Completed Features

- Mock Interview setup
- Role selection
- Difficulty selection
- Configurable question count
- Resume-aware interview flow
- Technical interview question generation
- Deterministic fallback question generation
- Interview session management
- One-question-at-a-time interview flow
- Answer submission
- Interview completion handling
- Existing session detection
- Continue existing interview
- Start new interview
- Interview results flow
- Sidebar navigation entry

---

## AI Interview Evaluation

Status

✅ COMPLETED

Completed Features

- Interview evaluation schema
- Overall interview score
- Technical score
- Relevance score
- Communication score
- Problem-solving score
- Strengths
- Weaknesses
- Improvement suggestions
- Question-by-question feedback
- Gemini evaluation path
- Deterministic fallback evaluation
- Evaluation caching within the active interview session
- Interview Results frontend

---

## AI Assistant / Chatbot

Status

✅ COMPLETED

Completed Features

- AI Assistant page
- Free-form chat input
- Suggested prompts
- Chat message API
- Authenticated chatbot access
- Resume context
- ATS context
- Job Match context
- Interview context
- Hybrid context routing
- High-confidence deterministic context detection
- Secondary deterministic context scoring
- Gemini context routing for ambiguous questions
- Structured context selection using Pydantic
- Context-aware final answer generation
- Gemini routing fallback
- Data-driven Resume fallback
- Data-driven ATS fallback
- Data-driven Job Match fallback
- Data-driven Interview fallback
- Multi-context fallback synthesis
- User-specific chat history persistence
- Chat history restoration after refresh
- Clear Chat functionality
- AI Assistant sidebar navigation entry

---

# Current API Endpoints

## General

- `GET /`
- `GET /health`

## Authentication

- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`

## Resume

- `POST /resume/upload`
- `GET /resume/info`
- `GET /resume/download`
- `DELETE /resume/delete`

## ATS

- `GET /ats/analysis`

## Job Match

- `POST /job-match/analyze`

## Mock Interview

- `POST /mock-interview/start`
- `POST /mock-interview/{session_id}/answer`
- `POST /mock-interview/{session_id}/evaluate`

## AI Assistant

- `POST /chat/message`

---

# Current Backend Architecture

```text
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
AI ProviderFactory
   ↓
Gemini Provider
   ↓
Feature-specific AI Services
   ├── Resume Parser
   ├── ATS Analysis
   ├── Job Requirement Extraction
   ├── Mock Interview Generation
   ├── Interview Evaluation
   └── AI Assistant
   ↓
Fallback / Deterministic Logic
   ├── Resume Parser Fallback
   ├── ATS Fallback
   ├── Job Match Fallback
   ├── Interview Question Fallback
   ├── Interview Evaluation Fallback
   └── Chatbot Data-driven Fallback
   ↓
Pydantic Schemas
   ↓
Storage