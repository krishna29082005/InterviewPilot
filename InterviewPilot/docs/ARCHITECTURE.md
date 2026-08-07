# InterviewPilot Architecture

## Overview

InterviewPilot is a full-stack AI-powered interview preparation platform with a Next.js frontend and a FastAPI backend.

The codebase is organized around a layered architecture:

- Frontend UI and state management
- REST API communication
- FastAPI route layer
- Service layer for business logic
- AI provider abstraction
- Pydantic schemas for validation
- Local file-based storage for resume artifacts

---

## Current High-Level Architecture

```
Browser
   ↓
Next.js Frontend
   ↓
REST API
   ↓
FastAPI Routes
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

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- TailwindCSS

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- JWT
- Passlib
- PyMuPDF
- Google Gemini

### Storage

- Local filesystem storage for uploaded resumes and parsed analysis JSON

---

## Current Folder Structure

```
InterviewPilot/
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       ├── context/
│       ├── hooks/
│       ├── lib/
│       └── types/
├── backend/
│   └── app/
│       ├── api/
│       │   ├── dependencies/
│       │   └── routes/
│       ├── ai/
│       │   ├── parsers/
│       │   ├── prompts/
│       │   ├── providers/
│       │   ├── schemas/
│       │   └── services/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       └── services/
└── docs/
```

---

## Backend Architecture

```
HTTP Request
   ↓
FastAPI Route
   ↓
Pydantic Validation
   ↓
Service Layer
   ↓
AI / Business Logic
   ↓
Database / File Storage
   ↓
JSON Response
```

### Route Layer

Responsibilities:

- Receives HTTP requests
- Injects dependencies
- Calls services
- Returns responses

Current routes:

- `GET /health`
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`
- `POST /resume/upload`
- `GET /resume/info`
- `GET /resume/download`
- `DELETE /resume/delete`
- `GET /ats/analysis`

### Service Layer

Responsibilities:

- Business logic
- Resume upload orchestration
- Resume analysis persistence
- ATS generation
- Fallback handling

### AI Layer

The AI layer is split into:

- `ProviderFactory`
- `GeminiProvider`
- Gemini prompt files
- Deterministic fallback parsers
- AI schemas

This keeps the rest of the app independent from the specific LLM provider.

### Schemas

Pydantic is used because it:

- validates structured AI output
- keeps response contracts stable
- prevents malformed data from reaching the frontend

### Storage

Resume PDFs and parsed analysis JSON are stored locally under:

- `backend/uploads/resumes/`

---

## AI Pipeline

### Resume Parsing

```
PDF Upload
   ↓
Extract Text
   ↓
Clean Text
   ↓
Gemini Resume Parser
   ↓
ResumeSchema
   ↓
Persist Analysis JSON
```

### ATS Analysis

```
ResumeSchema
   ↓
Gemini ATS Analysis
   ↓
ATSAnalysis
```

### Fallback Strategy

If Gemini fails because of:

- missing configuration
- invalid response
- 429 quota exhaustion
- 503 high-demand unavailability

the backend falls back to deterministic local logic.

The fallback strategy exists for both:

- resume parsing
- ATS analysis

This ensures the app remains usable even when the model is unavailable.

---

## Frontend Architecture

```
Browser
   ↓
Next.js Pages / Components
   ↓
Fetch API
   ↓
FastAPI
   ↓
JSON Response
   ↓
React State Update
```

Current frontend areas:

- Landing page
- Authentication pages
- Dashboard
- Resume dashboard
- ATS dashboard

---

## AI Provider Architecture

### ProviderFactory

`ProviderFactory` returns the configured LLM provider.

Current implementation:

- `gemini` → `GeminiProvider`

### GeminiProvider

Responsibilities:

- initialize the Gemini client
- send prompts to Gemini
- parse JSON output
- validate output with Pydantic
- raise typed AI exceptions on failure

---

## Resume Data Flow

```
Resume Upload
   ↓
Text Extraction
   ↓
Gemini Parser
   ↓
Fallback Parser if needed
   ↓
ResumeSchema
   ↓
Saved JSON analysis
   ↓
Resume dashboard
```

### Hyperlink Extraction

The PDF parser also extracts embedded link targets from the PDF annotations, so link labels like `GitHub` or `Live Demo` can still be resolved when the actual URL is stored in the document metadata.

---

## ATS Data Flow

```
ResumeSchema
   ↓
Gemini ATS Prompt
   ↓
Fallback ATS analysis if needed
   ↓
ATSAnalysis
   ↓
ATS dashboard
```

The ATS response includes:

- score
- summary
- strengths
- weaknesses
- missing keywords
- formatting issues
- recommendations

---

## Planned Areas

The following remain planned and are not yet implemented:

- Job description matching
- Mock interview engine
- Interview evaluation
- Analytics dashboard
- AI coaching workflow

