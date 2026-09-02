# Development Log

This document records the development progress of InterviewPilot throughout the project.

---

# Session 7

**Date**

2026-09-02

---

## Objective

Synchronize documentation and complete stabilization and end-to-end regression work for the v0.8.0 MVP.

## Stabilization Work

### Phase 1 - Backend Cleanup

- Removed debug print output and cleaned up logging.
- Reviewed security-sensitive output and exception handling.

### Phase 2 - AI Architecture Review

- Verified provider isolation, route/service separation, and Pydantic validation.
- Fixed async resume processing in the resume information route.

### Phase 3 - Persistence / State Review

- Reviewed file-backed state, browser state, and authenticated user scoping.
- Fixed stale ATS and Job Match cache invalidation.
- Added safe malformed-cache handling.
- Confirmed Mock Interview remains intentionally in-memory.

### Phase 4 - Frontend Polish

- Improved loading and error states for resume and ATS flows.
- Prevented cross-user chat localStorage carryover.
- Added password-toggle accessibility labels.
- Removed temporary debug output and dead navigation links.

### Phase 5 - E2E Regression Testing

- Verified authentication, resume, ATS, Job Match, Mock Interview, evaluation, and chat flows against the running application.
- Found and fixed a startup import regression.
- Verified cache invalidation, backend restart behavior, and user isolation.

## Validation Limitations

- `pytest` was unavailable in the current environment.
- Real browser automation was unavailable, so browser-only interaction checks could not be fully exercised.
- Direct Gemini execution was blocked by restricted network access during testing; deterministic and data-driven fallbacks were exercised.
- Existing ESLint issues remain in effect patterns and TypeScript typing.
- Passlib/bcrypt emits a compatibility warning, but password verification succeeds.

---

# Session 6

**Date**

2026-09-01

---

## Objective

Complete the remaining core InterviewPilot features:

- Mock Interview
- AI Interview Evaluation
- AI Assistant / Chatbot

Integrate the new features with the existing application and verify fallback behavior when Gemini is unavailable.

---

## Completed

### Mock Interview

- Implemented Mock Interview API
- Implemented interview session management
- Added role selection
- Added difficulty selection
- Added configurable question count
- Added resume-aware interview flow
- Added technical interview question generation
- Added deterministic fallback question generation
- Added one-question-at-a-time interview flow
- Added answer submission
- Added interview completion handling
- Added existing interview session detection
- Added continue or start-new-interview flow
- Integrated Mock Interview into the frontend
- Added Mock Interview to sidebar navigation

### AI Interview Evaluation

- Created structured interview evaluation schema
- Implemented interview evaluation service
- Added overall performance score
- Added technical score
- Added relevance score
- Added communication score
- Added problem-solving score
- Added strengths
- Added weaknesses
- Added improvement suggestions
- Added question-by-question feedback
- Added Gemini-first evaluation flow
- Added deterministic fallback evaluation
- Added interview evaluation endpoint
- Added evaluation caching within the interview session
- Added Interview Results frontend UI

### AI Assistant / Chatbot

- Created chatbot request and response schemas
- Created chatbot prompt architecture
- Implemented AI Assistant service
- Added free-form chatbot messaging
- Added suggested prompts
- Added AI Assistant frontend page
- Added AI Assistant to sidebar navigation
- Added `/chat/message` endpoint

### Chatbot Contexts

Implemented four InterviewPilot context sources:

- Resume
- ATS Analysis
- Job Match
- Interview

The chatbot can now use existing InterviewPilot data to answer personalized questions.

### Hybrid Context Routing

Implemented hybrid context routing consisting of:

1. High-confidence deterministic intent detection
2. Secondary deterministic context scoring
3. Gemini-based routing for ambiguous questions
4. Available-context fallback when Gemini routing is unavailable

Explicit questions are routed directly when confidence is high, while ambiguous questions can be classified by Gemini.

### Chatbot Fallback Architecture

Implemented fallback behavior for Gemini failures.

Added:

- Resume fallback responses
- ATS fallback responses
- Job Match fallback responses
- Interview fallback responses
- Multi-context fallback responses
- Data-driven fallback using stored InterviewPilot results

The fallback system continues to provide useful responses without depending entirely on Gemini.

### Data Persistence

- Added ATS analysis persistence
- Added cached ATS analysis retrieval
- Added latest Job Match result persistence
- Added job description persistence with Job Match results
- Added user-specific chatbot history using localStorage
- Added chatbot history restoration after page refresh
- Added Clear Chat functionality

### Frontend Integration

- Integrated Mock Interview with the authenticated dashboard layout
- Integrated AI Interview Evaluation with the interview completion flow
- Added Interview Results presentation
- Added AI Assistant to the main application navigation
- Added persistent chat conversation behavior
- Added context labels to chatbot responses

---

## Problems Faced

### Gemini Availability

Gemini repeatedly returned HTTP 503 `UNAVAILABLE` responses during development.

The error indicated provider-side model availability/high-demand conditions.

**Solution**

- Preserved Gemini as the primary AI provider.
- Added deterministic fallback question generation.
- Added deterministic fallback ATS analysis.
- Added deterministic fallback interview evaluation.
- Added data-driven chatbot fallback responses.
- Ensured the application continues operating when Gemini is unavailable.

---

### Chatbot Context Routing

Initially, some ATS questions were incorrectly routed to Job Match.

For example:

```text
Why could my ATS score be improved?
