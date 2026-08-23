# Development Log

This document records the development progress of InterviewPilot throughout the project.

---

# Session 5

**Date**

2026-08-23

---

## Objective

Synchronize documentation with the current InterviewPilot implementation.

---

## Completed

### Documentation

- Updated project context to reflect the current implemented feature set
- Updated architecture documentation to include job match and recommended roles flows
- Updated roadmap to mark resume parsing, ATS analysis, recommended roles, job matching, and the Job Match frontend as completed
- Updated changelog with the current release entry
- Updated frontend README to include the Job Match page

### Product

- Documented completed Job Description Matching flow
- Documented ATS-driven Recommended Roles / Career Fit behavior
- Documented fallback handling for Gemini 429 and 503 responses
- Kept Mock Interview and AI Interview Evaluation explicitly planned

---

## Notes

- No application source code was modified for this session.
- Documentation now distinguishes implemented features from planned features more clearly.
- Gemini availability remains a non-blocking dependency because fallback logic is documented as part of the supported architecture.

---

## Next Session

- Mock Interview design and implementation
- AI Interview Evaluation planning
- Optional documentation polish after the next feature lands

---

# Session 1

**Date**

2026-07-05

---

## Objective

Initialize the project repository and frontend.

---

## Completed

### Repository

- Created GitHub repository
- Created monorepo structure

### Frontend

- Initialized Next.js
- Configured TypeScript
- Configured Tailwind CSS
- Configured ESLint
- Created landing page
- Started development server

### Git

- Created first Git commit

---

## Decisions

- Next.js instead of Vite
- FastAPI instead of Flask
- Monorepo architecture
- Tailwind CSS
- App Router

---

## Problems Faced

- Node PATH issue
- Nested repository issue
- README directory issue

---

## Learnings

- Git workflow
- Professional repository setup
- Next.js initialization

---

## Next Session

- Initialize FastAPI backend
- Create first API
- Connect frontend and backend

---

# Session 2

**Date**

2026-07-06

---

## Objective

Initialize the FastAPI backend and establish frontend-backend communication.

---

## Completed

### Backend

- Created Python virtual environment
- Installed FastAPI
- Installed Uvicorn
- Generated `requirements.txt`
- Created backend folder structure
- Created FastAPI application
- Added Root endpoint (`/`)
- Added Health endpoint (`/health`)
- Configured APIRouter
- Configured Swagger/OpenAPI
- Configured CORS middleware

### Frontend

- Converted landing page into a Client Component
- Learned React `useState`
- Learned React `useEffect`
- Connected frontend to FastAPI backend
- Displayed backend health status

### Git

- Updated `.gitignore`
- Removed virtual environment from Git tracking
- Created cleanup commit
- Pushed changes to GitHub

---

## Decisions

- Modular routing using APIRouter
- Keep `main.py` minimal
- Feature-based routing
- Configure CORS during development
- Never commit virtual environments

---

## Problems Faced

### Virtual Environment tracked by Git

**Solution**

- Updated `.gitignore`

```bash
git rm -r --cached backend/.venv
```

---

### Frontend could not reach backend

**Cause**

Same-Origin Policy

**Solution**

Configured `CORSMiddleware`

---

### Git commit confusion

**Solution**

Verified commit history using

```bash
git log --oneline
```

---

## Learnings

### FastAPI

- APIRouter
- OpenAPI
- Swagger

### React

- Client Components
- useState
- useEffect
- Fetch API

### Backend

- REST APIs
- JSON Responses
- CORS

### Git

- `.gitignore`
- `git rm --cached`

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

JSON Response

↓

React UI
```

---

## Next Session

- Authentication Module
- PostgreSQL
- SQLAlchemy

---

# Session 3

**Date**

2026-07-07

---

## Objective

Build a production-style authentication system backed by PostgreSQL.

---

## Completed

### Database

- Installed PostgreSQL
- Created `interviewpilot` database
- Connected SQLAlchemy
- Configured database sessions
- Created database initialization script
- Generated first database table (`users`)

### Models

- Created User model
- Designed user table schema

### Authentication

- Created Authentication Router
- Created Signup API
- Added Pydantic request validation
- Implemented Service Layer
- Connected service with PostgreSQL
- Stored first user in database

### Security

- Implemented bcrypt password hashing
- Prevented duplicate usernames
- Prevented duplicate emails
- Added HTTP 409 Conflict responses
- Added database transaction rollback

### Testing

- Verified API using Swagger UI
- Verified database records using PostgreSQL
- Successfully stored first real user

---

## Decisions

- Layered Backend Architecture
- Route → Schema → Service → Database
- SQLAlchemy ORM
- PostgreSQL
- bcrypt password hashing
- Database sessions using dependency injection

---

## Problems Faced

### PostgreSQL PATH issue

**Solution**

Added PostgreSQL `bin` directory to Windows PATH.

---

### Missing `email-validator`

**Solution**

Installed:

```bash
pip install email-validator
```

---

### bcrypt compatibility warning

**Solution**

Verified hashing worked correctly.

---

### Duplicate username crash

**Solution**

Added application-level validation before database insertion.

---

## Learnings

### Authentication

- Password hashing
- HTTP status codes
- Duplicate validation

### SQLAlchemy

- Models
- Sessions
- Transactions
- ORM workflow

### PostgreSQL

- Database creation
- Table creation
- SQL verification

### Backend Engineering

- Layered Architecture
- Separation of Concerns
- Dependency Injection

---

## Architecture Achieved

```
Client

↓

FastAPI Route

↓

Pydantic Schema

↓

Service Layer

↓

SQLAlchemy ORM

↓

PostgreSQL

↓

JSON Response
```

---

## Next Session

- Login API
- JWT Authentication
- Protected Routes
- Current User Endpoint

---

# Session 4

**Date**

2026-07-08

---

## Objective

Complete the Authentication Module.

---

## Completed

### Authentication

- Implemented Login API
- Implemented OAuth2 Password Flow
- Implemented JWT Token Generation
- Implemented JWT Verification
- Created Protected Endpoints
- Implemented Current User Dependency
- Implemented `/auth/me`
- Added response models
- Centralized security utilities into `core/security.py`
- Moved `SECRET_KEY` to environment variables
- Added function return type hints
- Cleaned imports and project structure

### Security

- Password Hashing
- Password Verification
- JWT Access Tokens
- Protected Routes
- OAuth2 Integration

### Testing

Completed full regression testing.

Passed all 8 tests:

- ✅ Signup
- ✅ Duplicate Email
- ✅ Duplicate Username
- ✅ Login
- ✅ JWT Generation
- ✅ Protected Route (`/auth/me`)
- ✅ Invalid Password
- ✅ Unauthorized Access

---

## Decisions

- Adopt FastAPI OAuth2 Password Flow
- Store email inside JWT subject (`sub`)
- Centralize all security logic inside `core/security.py`
- Every endpoint should have request and response models
- Freeze completed modules after testing

---

## Learnings

- OAuth2 Password Flow
- JWT Authentication
- Dependency Injection
- Response Models
- Security Layer Design
- Production Refactoring
- Regression Testing

---

## Current Status

✅ Authentication Module Completed

---

# Development Log

## Version 0.4.0 (11-07-2026)

### Authentication
- Improved authentication flow
- Automatic login after signup
- Persistent authentication using AuthContext
- Dashboard route protection
- Logout functionality

### Dashboard
- Redesigned dashboard layout
- Added professional sidebar navigation
- Created reusable DashboardCard component
- Added Resume, Interviews, Analytics and Quick Actions sections

### Resume Module
- Built Resume Management page
- Resume upload UI
- PDF validation
- File selection preview
- Resume upload API integration
- Backend resume storage
- Success and error notifications
- Resume management card
- Resume download/replace/delete UI (frontend scaffold)

### Backend
- Resume upload endpoint
- Authentication middleware
- JWT verification improvements
- Uploads folder integration

### Bug Fixes
- Fixed routing issues
- Fixed login redirect
- Fixed dashboard rendering
- Fixed token restoration
- Fixed resume upload authentication
- Fixed backend endpoint registration

### Next Milestone
- Resume Management APIs
- Resume AI Analysis
- ATS Score Generation
- Skill Extraction
- AI Interview Generation

Last Updated: July 19, 2026

---

# Overall Progress

## Backend
- [x] FastAPI Project Setup
- [x] JWT Authentication
- [x] User Management
- [x] Protected APIs

## AI Architecture
- [x] Modular AI Architecture
- [x] Provider Abstraction
- [x] Gemini Provider
- [x] Prompt Management
- [x] AI Schemas
- [x] Resume Processing Pipeline

## Resume Module
- [x] Resume Upload
- [x] Resume Download
- [x] Resume Delete
- [x] Resume Information API
- [x] Resume Persistence
- [x] Resume Analysis Storage

## Dashboard
- [x] Resume Upload UI
- [x] Resume Details
- [x] Download Resume
- [x] Delete Resume

---

# Current Resume Pipeline

User Upload
        ↓
Save PDF
        ↓
Extract Text (PyMuPDF)
        ↓
Clean Text
        ↓
Prompt Builder
        ↓
Gemini
        ↓
Pydantic Validation
        ↓
Store JSON Analysis
        ↓
Dashboard Display

---

Current Status

🟢 Stable

Known Issue:
- Some LaTeX-generated resumes produce PDF extraction artifacts (e.g., isolated characters like "R").
- This originates from the PDF text layer rather than Gemini.

---

# Recent Development

## Resume Intelligence Update

### Completed

- Added Gemini-first resume parsing with deterministic fallback parsing
- Added Gemini-first ATS analysis with deterministic fallback analysis
- Added PDF hyperlink extraction from embedded annotations
- Added resume regeneration when the stored analysis JSON is missing
- Improved link parsing for LinkedIn, GitHub, LeetCode, and portfolio fields
- Redesigned the resume dashboard into a structured report layout
- Redesigned the ATS dashboard for cleaner score and insight display

### Notes

- Gemini is still attempted first for both resume parsing and ATS analysis.
- If Gemini is rate-limited or unavailable, the fallback path keeps the app usable.
- The backend now logs when Gemini falls back so the active path is visible during development.

## Current Resume Pipeline

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
Persist JSON Analysis
      ↓
ATS Analysis
      ↓
Gemini ATS Analysis
      ↓
ATSAnalysis
```

## Fallback Strategy

- Resume parsing falls back to a deterministic local parser when Gemini raises an AI error.
- ATS analysis falls back to a local ATS scorer when Gemini raises an AI error.
- PDF hyperlinks are extracted directly from PDF annotations so visible labels like `GitHub` and `Live Demo` can be resolved when possible.

## Current Focus

- Documentation sync
- Resume parser accuracy
- Better link extraction
- Stable Gemini-first behavior with safe fallbacks
