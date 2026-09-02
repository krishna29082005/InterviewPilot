import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.ai.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
)
from app.ai.schemas.resume import ResumeSchema
from app.ai.services.chat import chat_with_candidate
from app.api.dependencies.auth import get_current_user
from app.services.ats import get_ats_analysis
from app.services.job_match import get_job_match_result
from app.services.resume import get_resume_analysis
from app.services.mock_interview import (
    _sessions,
    InterviewSession,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


def _get_user_interview(
    user_id: int,
) -> InterviewSession | None:
    """
    Return the most recent interview session belonging
    to the authenticated user.

    The current interview implementation uses an in-memory
    session store, so this only works while the backend process
    is alive.
    """

    user_sessions = [
        session
        for session in _sessions.values()
        if session.user_id == user_id
    ]

    if not user_sessions:
        return None

    # Use insertion order to get the most recently created session.
    return user_sessions[-1]


@router.post(
    "/message",
    response_model=ChatMessageResponse,
)
async def send_chat_message(
    request: ChatMessageRequest,
    current_user=Depends(get_current_user),
):
    """
    Send a context-aware message to the InterviewPilot AI assistant.
    """

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    # ------------------------------------------------------
    # 1. Load resume
    # ------------------------------------------------------

    resume = None

    resume_analysis = get_resume_analysis(
        current_user.id
    )

    if resume_analysis is not None:
        try:
            resume = ResumeSchema.model_validate(
                resume_analysis
            )

        except ValidationError as exc:
            logger.warning(
                "Stored resume analysis is invalid for chatbot: %s",
                exc,
            )

    # ------------------------------------------------------
    # 2. Load ATS analysis
    # ------------------------------------------------------

    ats_analysis = get_ats_analysis(
        current_user.id
    )

    # ------------------------------------------------------
    # 3. Load latest Job Match result
    # ------------------------------------------------------

    job_match = get_job_match_result(
        current_user.id
    )

    # ------------------------------------------------------
    # 4. Load current interview session
    # ------------------------------------------------------

    interview = None

    current_interview = _get_user_interview(
        current_user.id
    )

    if current_interview is not None:
        interview = {
            "session_id": current_interview.session_id,
            "role": current_interview.role,
            "difficulty": current_interview.difficulty,
            "status": current_interview.status,
            "questions": [
                {
                    "question": question.question,
                    "category": question.category,
                    "difficulty": question.difficulty,
                }
                for question in current_interview.questions
            ],
            "answers": current_interview.answers,
            "evaluation": (
                current_interview.evaluation.model_dump()
                if current_interview.evaluation is not None
                else None
            ),
        }

    # ------------------------------------------------------
    # 5. Log available chatbot contexts
    # ------------------------------------------------------

    available_contexts = []

    if resume is not None:
        available_contexts.append("resume")

    if ats_analysis is not None:
        available_contexts.append("ats_analysis")

    if job_match is not None:
        available_contexts.append("job_match")

    if interview is not None:
        available_contexts.append("interview")

    logger.debug(
        "Chat contexts available for user %s: %s",
        current_user.id,
        available_contexts,
    )

    # ------------------------------------------------------
    # 6. Generate chatbot response
    # ------------------------------------------------------

    try:
        response = await chat_with_candidate(
            message=message,
            resume=resume,
            ats_analysis=ats_analysis,
            job_match=job_match,
            interview=interview,
        )

        return response

    except Exception as exc:
        logger.exception(
            "Chatbot request failed: %s",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to process chatbot message.",
        ) from exc