# InterviewPilot

AI-powered interview preparation platform.

## Features

### Authentication

- JWT Signup
- JWT Login
- Protected routes
- Current user endpoint

### Resume Management

- Resume upload
- Resume download
- Resume delete
- Resume information endpoint
- Resume dashboard

### Resume Parsing

- Gemini Resume Parser
- Fallback Resume Parser
- ResumeSchema validation
- Deterministic parsing
- PDF text extraction
- PDF hyperlink extraction
- Resume regeneration when analysis is missing

### ATS Analysis

- Gemini ATS Analysis
- Fallback ATS Analysis
- ATS score
- Summary
- Strengths
- Weaknesses
- Missing keywords
- Formatting issues
- Recommendations

### AI Architecture

- Provider abstraction
- ProviderFactory
- Prompt management
- Pydantic validation
- Gemini-first execution
- Safe fallback strategy

## Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- JWT
- Passlib
- PyMuPDF
- Google Gemini
- Local storage

### Frontend

- Next.js
- React
- TypeScript
- TailwindCSS
- Fetch API

## AI Workflow

### Resume Upload

```
PDF Upload
      ↓
Extract Text
      ↓
Clean Text
      ↓
Gemini
      ↓
ResumeSchema
      ↓
Resume Dashboard
```

### ATS Analysis

```
ResumeSchema
      ↓
Gemini
      ↓
ATSAnalysis
```

### Fallback Strategy

If Gemini is unavailable, rate-limited, or returns an invalid response, the backend falls back to deterministic local parsing and analysis so the app does not crash.

## Architecture

```
Frontend
      ↓
REST API
      ↓
FastAPI
      ↓
AI Services
      ↓
Gemini Provider
      ↓
Fallback Parser
      ↓
Pydantic Schemas
```

### Service Layer

- Keeps route handlers thin
- Handles resume processing and ATS generation
- Coordinates Gemini and fallback flows
- Stores resume analysis locally

### Why Pydantic

- Validates resume and ATS output
- Keeps AI responses structured
- Prevents invalid data from reaching the frontend

## API Endpoints

### Authentication

#### `POST /auth/signup`

Creates a new user.

Request body:

```json
{
  "name": "Krishna Mehra",
  "email": "krishna@example.com",
  "password": "secret123"
}
```

Response:

```json
{
  "message": "User created successfully."
}
```

#### `POST /auth/login`

Logs in a user using OAuth2 password form data.

Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

#### `GET /auth/me`

Returns the authenticated user.

Response:

```json
{
  "id": 1,
  "username": "krishna",
  "email": "krishna@example.com"
}
```

### Resume

#### `POST /resume/upload`

Uploads a PDF resume and runs parsing.

#### `GET /resume/info`

Returns resume metadata and parsed analysis.

#### `GET /resume/download`

Downloads the uploaded resume PDF.

#### `DELETE /resume/delete`

Deletes the stored resume and analysis.

### ATS

#### `GET /ats/analysis`

Returns ATS analysis for the uploaded resume.

## Project Status

### Completed

- Authentication
- Resume Upload
- Resume Parsing
- Fallback Resume Parser
- ATS Analysis
- Fallback ATS Analysis
- Resume Dashboard
- ATS Dashboard
- Hyperlink extraction
- Resume regeneration

### Upcoming

- Job Description Matching
- Mock Interview
- AI Interview Evaluator
- Analytics Dashboard

## Screenshots

Add screenshots here when available.

- Resume dashboard
- ATS dashboard
- Login page
- Signup page

