from fastapi import APIRouter, Depends, HTTPException
from app.ai.services.interview_evaluation import evaluate_interview
from app.ai.schemas.mock_interview import (
    MockInterviewAnswerRequest,
    MockInterviewResponse,
    MockInterviewStartRequest,
)
from app.ai.schemas.resume import ResumeSchema
from app.ai.services.mock_interview import (
    generate_interview_questions,
)
from app.api.dependencies.auth import get_current_user
from app.services.mock_interview import (
    create_interview_session,
    get_interview_session,
    submit_interview_answer,
)
from app.services.resume import get_resume_analysis


router = APIRouter(
    prefix="/mock-interview",
    tags=["Mock Interview"],
)


@router.post(
    "/start",
    response_model=MockInterviewResponse,
)
async def start_mock_interview(
    request: MockInterviewStartRequest,
    current_user=Depends(get_current_user),
):
    """
    Start a new mock interview session.
    """

    resume_analysis = get_resume_analysis(
        current_user.id
    )

    if resume_analysis is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Resume analysis not found. "
                "Please upload your resume first."
            ),
        )

    try:
        resume = ResumeSchema.model_validate(
            resume_analysis
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Stored resume analysis is invalid.",
        ) from exc

    questions = await generate_interview_questions(
        resume=resume,
        role=request.role.strip(),
        difficulty=request.difficulty,
        question_count=request.question_count,
    )

    if not questions:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate interview questions.",
        )

    session = create_interview_session(
        user_id=current_user.id,
        role=request.role.strip(),
        difficulty=request.difficulty,
        questions=questions,
    )

    current_question = session.current_question

    if current_question is None:
        raise HTTPException(
            status_code=500,
            detail="Interview session contains no questions.",
        )

    return MockInterviewResponse(
        session_id=session.session_id,
        role=session.role,
        difficulty=session.difficulty,
        question_number=session.current_question_index + 1,
        total_questions=session.total_questions,
        question=current_question.question,
        category=current_question.category,
        status=session.status,
    )


@router.post(
    "/{session_id}/answer",
    response_model=MockInterviewResponse,
)
async def answer_mock_interview_question(
    session_id: str,
    request: MockInterviewAnswerRequest,
    current_user=Depends(get_current_user),
):
    """
    Submit the current answer and move to the next question.
    """

    answer = request.answer.strip()

    session = get_interview_session(
        session_id=session_id,
        user_id=current_user.id,
    )

    session = submit_interview_answer(
        session=session,
        answer=answer,
    )

    if session.status == "completed":
        return MockInterviewResponse(
            session_id=session.session_id,
            role=session.role,
            difficulty=session.difficulty,
            question_number=session.total_questions,
            total_questions=session.total_questions,
            question=None,
            category=None,
            status="completed",
        )

    next_question = session.current_question

    if next_question is None:
        raise HTTPException(
            status_code=500,
            detail="Next question could not be found.",
        )

    return MockInterviewResponse(
        session_id=session.session_id,
        role=session.role,
        difficulty=session.difficulty,
        question_number=session.current_question_index + 1,
        total_questions=session.total_questions,
        question=next_question.question,
        category=next_question.category,
        status=session.status,
    )


@router.get(
    "/{session_id}",
    response_model=MockInterviewResponse,
)
async def get_mock_interview_session(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Retrieve the current state of an interview session.
    """

    session = get_interview_session(
        session_id=session_id,
        user_id=current_user.id,
    )

    if session.status == "completed":
        return MockInterviewResponse(
            session_id=session.session_id,
            role=session.role,
            difficulty=session.difficulty,
            question_number=session.total_questions,
            total_questions=session.total_questions,
            question=None,
            category=None,
            status="completed",
        )

    current_question = session.current_question

    if current_question is None:
        raise HTTPException(
            status_code=500,
            detail="Current question could not be found.",
        )

    return MockInterviewResponse(
        session_id=session.session_id,
        role=session.role,
        difficulty=session.difficulty,
        question_number=session.current_question_index + 1,
        total_questions=session.total_questions,
        question=current_question.question,
        category=current_question.category,
        status=session.status,
    )

# ==========================================================
# Evaluate Completed Interview
# ==========================================================

@router.post("/{session_id}/evaluate")
async def evaluate_mock_interview(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Evaluate a completed mock interview.

    If the interview has already been evaluated, return the
    stored evaluation instead of generating it again.
    """

    # ------------------------------------------------------
    # Get session
    # ------------------------------------------------------

    session = get_interview_session(
        session_id=session_id,
        user_id=current_user.id,
    )

    # ------------------------------------------------------
    # Interview must be completed
    # ------------------------------------------------------

    if session.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=(
                "Interview must be completed "
                "before evaluation."
            ),
        )

    # ------------------------------------------------------
    # Return cached evaluation if available
    # ------------------------------------------------------

    if session.evaluation is not None:
        return session.evaluation

    # ------------------------------------------------------
    # Generate evaluation
    # ------------------------------------------------------

    evaluation = await evaluate_interview(
        role=session.role,
        questions=session.questions,
        answers=session.answers,
    )

    # ------------------------------------------------------
    # Cache evaluation in session
    # ------------------------------------------------------

    session.evaluation = evaluation

    return evaluation