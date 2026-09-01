from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chat import router as chat_router
from app.api.routes.job_match import router as job_match_router
from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.resume import router as resume_router
from app.api.routes.ats import router as ats_router
from app.api.routes.mock_interview import (
    router as mock_interview_router,
)
app = FastAPI(
    title="InterviewPilot API",
    description="Backend API for InterviewPilot - AI Powered Interview Preparation Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],#this allows our frontend which is rpesent in another origiin to access our backend API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to InterviewPilot API 🚀"
    }
app.include_router(chat_router)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(job_match_router)
app.include_router(
    mock_interview_router
)