# Changelog

All notable changes to InterviewPilot will be documented in this file.

The project follows Semantic Versioning.

---

# v0.8.0

Release Date: 01 September 2026

## Stabilization / Polish

The following verified stabilization work was completed within v0.8.0 after the core feature work. These are maintenance and reliability changes, not new product features.

### Backend

- Removed debug output and standardized application logging.
- Improved exception handling around AI providers and persistence boundaries.
- Isolated Gemini SDK usage in the provider layer.
- Fixed async resume processing in the resume information route.
- Invalidated stale ATS and Job Match caches when a resume is replaced or deleted.
- Made malformed resume, ATS, and Job Match cache data fail safely.
- Verified authenticated user isolation across file-backed state and interview sessions.
- Fixed a startup import regression discovered during end-to-end testing.

### Frontend

- Added resume upload loading and duplicate-submit protection.
- Improved ATS error-state presentation.
- Added localStorage safety for user switching and malformed chat history.
- Added accessible labels to password visibility controls.
- Removed temporary debug logging and dead navigation targets.

### Verification

- Completed live regression checks for authentication, resume upload, ATS, Job Match, Mock Interview, evaluation, and chat.
- Verified cache invalidation, backend restart behavior, and cross-user isolation.
- Backend compile and frontend production build passed.
- pytest was unavailable in the test environment, browser automation was unavailable, and direct Gemini execution was blocked by restricted network access during testing.

## Added

### Mock Interview

- Mock Interview API
- Interview session management
- Role-specific interview question generation
- Difficulty selection
- Configurable interview question count
- One-question-at-a-time interview flow
- Interview answer submission
- Interview completion handling

### AI Interview Evaluation

- Interview evaluation API
- Overall interview score
- Technical performance score
- Relevance score
- Communication score
- Problem-solving score
- Interview strengths
- Interview weaknesses
- Improvement suggestions
- Question-by-question feedback
- Deterministic fallback interview evaluation

### AI Assistant / Chatbot

- AI Assistant chatbot
- Free-form conversational interface
- Suggested prompts for Resume, ATS, Job Match, and Interview topics
- User-specific chat history persistence
- Clear Chat functionality
- AI Assistant frontend page
- AI Assistant sidebar navigation entry

### Context-Aware Chatbot

- Resume context
- ATS analysis context
- Job Match context
- Interview context
- Hybrid context routing
- Deterministic high-confidence intent detection
- Secondary deterministic context scoring
- Gemini-based context routing for ambiguous queries
- Structured context selection using Pydantic validation
- Context-aware final response generation

### Chatbot Fallbacks

- Gemini context-routing fallback
- Data-driven Resume fallback
- Data-driven ATS fallback
- Data-driven Job Match fallback
- Data-driven Interview fallback
- Multi-context fallback synthesis
- Graceful chatbot behavior during Gemini 503 responses

### Data Persistence

- Latest ATS analysis persistence
- Latest Job Match result persistence
- Job description persistence with Job Match analysis
- User-specific chatbot history persistence using localStorage

## Changed

- Expanded the AI architecture to support Mock Interview and AI Assistant workflows
- Expanded fallback architecture beyond Resume and ATS processing
- Added context-aware data selection before chatbot response generation
- Improved chatbot routing for overlapping natural-language queries
- Improved handling of ambiguous chatbot questions
- Integrated AI Assistant into the main authenticated application shell
- Integrated Mock Interview into the main application navigation
- Updated frontend API layer for chatbot and interview evaluation functionality
- Added cached ATS analysis retrieval to avoid repeated generation
- Added cached Job Match result retrieval for chatbot context

## Fixed

- Fixed incorrect chatbot routing of ATS questions to Job Match context
- Fixed incorrect chatbot routing of Resume questions to Job Match context
- Fixed deterministic routing threshold issue for explicit ATS queries
- Fixed multi-context fallback responses being returned as unrelated concatenated answers
- Fixed chatbot refresh behavior where previous conversation messages disappeared
- Fixed missing ATS context in the chatbot route
- Fixed Job Match result availability for chatbot context
- Fixed interview completion flow
- Fixed interview evaluation fallback behavior when Gemini is unavailable
- Fixed navigation integration for Mock Interview and AI Assistant

## Notes

- Gemini may temporarily return 503 responses because of provider-side availability or demand.
- InterviewPilot continues to operate through deterministic and data-driven fallback mechanisms when Gemini is unavailable.
- The chatbot uses deterministic routing for high-confidence queries and Gemini routing for ambiguous queries when the provider is available.
- Chat history currently persists locally per authenticated user through browser localStorage.

---

# v0.7.0

Release Date: 23 August 2026

## Added

### Job Match

- Job Description Matching API
- Job Match frontend page
- Sidebar navigation entry for Job Match
- Deterministic job requirement matching
- Fallback job requirement parsing

### Career Fit

- ATS-driven role recommendations
- Gemini role recommendation extraction
- Deterministic fallback role detection
- Career Fit / Recommended Roles UI

### Documentation

- Updated architecture documentation
- Updated project context
- Updated roadmap
- Updated development log
- Updated frontend README

## Changed

- Expanded fallback strategy documentation to include job matching
- Clarified implemented versus planned features across docs
- Aligned project status with the current codebase

## Fixed

- Documentation drift between roadmap, changelog, project context, and architecture notes
- Incomplete feature status descriptions for ATS and job matching related work

---

# v0.6.0

Release Date: 07 August 2026

## Added

### Resume Intelligence

- Fallback Resume Parser
- Resume regeneration when analysis JSON is missing
- PDF hyperlink extraction
- Better resume parsing prompts for link extraction

### ATS Analysis

- Fallback ATS analysis
- Gemini-first ATS generation with safe fallback

### Frontend

- Resume dashboard redesign
- ATS dashboard redesign
- Cleaner structured resume analysis UI
- Better link rendering

### Documentation

- Updated project architecture documentation
- Updated roadmap
- Updated project context

## Improved

- Gemini failure handling
- Resume parsing resilience
- ATS resilience during 429 and 503 responses
- Local file-based analysis regeneration

---

# v0.4.0

## Added

### Resume Module

- Authentication persistence
- Protected dashboard
- Professional dashboard UI
- Sidebar navigation
- Resume upload page
- PDF upload support
- Resume storage backend
- Resume upload notifications
- Resume management card

### Resume AI Architecture

- Modular AI architecture
- Gemini provider abstraction
- Resume parser pipeline
- Prompt management
- Pydantic response validation
- Resume analysis persistence
- Resume information API
- Resume download API
- Resume deletion API
- Dashboard integration

## Improved

- Login flow
- Signup flow
- Dashboard UX
- Error handling
- Authentication state restoration
- Resume upload flow
- AI processing pipeline
- Provider initialization
- Resume overwrite handling
- Overall project structure

## Fixed

- Login routing
- Dashboard rendering
- JWT authentication
- Resume upload integration
- Provider initialization bug
- Resume overwrite issues
- Dashboard synchronization
- Resume deletion cleanup
- AI parsing pipeline verification

## Notes

- Investigated incorrect parsing of "Krishna Mehra R".
- Root cause traced to LaTeX-generated PDF text layer artifacts during PDF extraction.
- Confirmed Gemini correctly parsed the extracted text and was not the source of the issue.

---

# v0.3.0

Release Date: 08 July 2026

## Added

### Authentication

- User Registration API
- User Login API
- OAuth2 Password Flow
- JWT Authentication
- Protected API Endpoints
- Current User Endpoint (`GET /auth/me`)
- Password Hashing using bcrypt
- Duplicate Username Validation
- Duplicate Email Validation
- JWT Verification
- Database Transaction Rollback

### Database

- PostgreSQL Integration
- SQLAlchemy ORM
- User Database Model
- Database Session Management
- Database Initialization Script

### API

- Authentication Router
- Signup Endpoint (`POST /auth/signup`)
- Login Endpoint (`POST /auth/login`)
- Current User Endpoint (`GET /auth/me`)

---

# v0.2.0

Release Date: July 2026

## Added

### Backend

- Initialized FastAPI backend
- Professional backend folder structure
- Modular API architecture using APIRouter
- Root (`/`) endpoint
- Health (`/health`) endpoint
- Automatic Swagger/OpenAPI documentation
- CORS middleware for frontend-backend communication

### Frontend

- Connected Next.js frontend with FastAPI backend
- Added backend health status indicator
- Implemented API communication using Fetch API
- Introduced React `useState` and `useEffect`

### Project

- Configured Python virtual environment
- Added backend dependencies (`requirements.txt`)
- Updated `.gitignore` for Python development
- Established first full-stack communication

---

# v0.1.0

Release Date: July 2026

## Added

### Repository

- GitHub Repository
- Monorepo Architecture
- Professional Project Structure

### Frontend

- Initialized Next.js
- TypeScript Configuration
- Tailwind CSS
- ESLint Configuration
- App Router
- Landing Page

### Documentation

- PROJECT_CONTEXT.md
- ARCHITECTURE.md
- DEVLOG.md
- CHANGELOG.md
- ROADMAP.md
