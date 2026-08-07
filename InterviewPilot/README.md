# InterviewPilot

AI-powered interview preparation platform.

## Features

### Authentication

- JWT Login
- Protected APIs
- User Management

### Resume Module

- Upload Resume
- Download Resume
- Delete Resume
- Resume Dashboard
- AI Resume Parsing
- Resume Metadata
- Structured Resume Analysis

### AI

- Gemini Integration
- Modular Provider Architecture
- Prompt Management
- Pydantic Validation
- Structured Resume Extraction

## Resume Processing Architecture

PDF Resume
      ↓
PyMuPDF Text Extraction
      ↓
Text Cleaning
      ↓
Prompt Builder
      ↓
Gemini
      ↓
Pydantic Validation
      ↓
JSON Analysis
      ↓
Dashboard