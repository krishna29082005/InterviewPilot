# Changelog

All notable changes to InterviewPilot will be documented in this file.

The project follows Semantic Versioning.

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

## Added

### Authentication

- User Registration API
- Layered Authentication Architecture
- Pydantic Request Validation
- Service Layer
- User Database Model
- Password Hashing using bcrypt
- Duplicate Username Validation
- Duplicate Email Validation
- Database Transaction Rollback
- Database Session Management

### Database

- PostgreSQL Integration
- SQLAlchemy ORM
- User Table
- Database Initialization Script

### API

- Authentication Router
- Signup Endpoint (`POST /auth/signup`)

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

---

# Upcoming (v0.4.0)

## Authentication

- User Login
- JWT Authentication
- Protected Routes
- Authentication Middleware

---

## Future Releases

### v0.5.0

- Resume Upload
- PDF Parsing
- Skill Extraction

### v0.6.0

- AI Interview Generation
- LLM Evaluation
- Feedback Engine

### v0.7.0

- Dashboard
- Progress Analytics
- Interview History
- Performance Tracking

### v1.0.0

- Production Deployment
- Docker
- CI/CD
- Monitoring
- Complete SaaS Platform