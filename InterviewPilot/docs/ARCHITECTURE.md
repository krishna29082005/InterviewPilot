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
Fallback Parser / Fallback ATS / Fallback Job Match
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
- `POST /job-match/analyze`
- `POST /mock-interview/start`
- `GET /mock-interview/{session_id}`
- `POST /mock-interview/{session_id}/answer`
- `POST /mock-interview/{session_id}/evaluate`
- `POST /chat/message`

### Service Layer

Responsibilities:

- Business logic
- Resume upload orchestration
- Resume analysis persistence
- ATS generation
- Job description matching
- Mock Interview question generation and session state
- Interview evaluation
- AI Assistant context routing and response generation
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
- job description matching
- Mock Interview question generation
- interview evaluation
- AI Assistant responses

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
- Job Match page
- Mock Interview page
- AI Assistant page

---

## AI Provider Architecture

### ProviderFactory

`ProviderFactory` returns the configured LLM provider.

Current implementation:

- `gemini` → `GeminiProvider`

### AI Design Notes

- The application does not use LangChain.
- Services call the configured provider directly through `ProviderFactory`.
- Structured outputs are validated with Pydantic models before reaching the API layer.

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

## Recommended Roles Flow

```
ResumeSchema
   ↓
ATS Service
   ↓
Gemini role recommendation
   or fallback role detection
   ↓
RecommendedRole[]
   ↓
Career Fit UI
```

The role recommendation layer currently highlights evidence for:

- AI/ML Engineer
- Backend Engineer
- Frontend Engineer
- Data Scientist
- DevOps / Cloud Engineer
- Software Engineer fallback

---

## Job Match Data Flow

```
Job Description
   ↓
Job Match Router
   ↓
Job Match AI Service
   ↓
Gemini requirement extraction
   ↓
Fallback parser if needed
   ↓
JobRequirements
   ↓
Deterministic matching service
   ↓
JobMatchAnalysis
   ↓
Frontend
```

The job match response includes:

- match score
- matching skills
- missing skills
- matching keywords
- missing keywords
- strengths
- gaps
- recommendations

---

## Current Persistence Notes

- Resume PDF: `backend/uploads/resumes/{user_id}_resume.pdf`
- Resume analysis: `{user_id}_analysis.json`
- ATS analysis: `{user_id}_ats_analysis.json`
- Job Match result: `{user_id}_job_match.json`
- Mock Interview sessions and evaluations: in-memory only
- Chat history: user-scoped browser localStorage

Resume, ATS, and Job Match files survive backend restart. Mock Interview sessions and evaluations do not. Chat history survives browser refresh.

## Planned Areas

The following remain planned and are not yet implemented:

- Analytics dashboard
- Persistent interview history
- Production hardening
- DevOps and deployment
