from uuid import uuid4

from fastapi import HTTPException

from app.ai.schemas.mock_interview import (
    InterviewQuestion,
)


class InterviewSession:
    """
    Represents the current state of one mock interview.
    """

    def __init__(
        self,
        session_id: str,
        user_id: int,
        role: str,
        difficulty: str,
        questions: list[InterviewQuestion],
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.role = role
        self.difficulty = difficulty

        self.questions = questions

        self.current_question_index = 0

        self.answers: list[str] = []

        self.status = "active"
        self.evaluation = None

    @property
    def total_questions(self) -> int:
        return len(self.questions)

    @property
    def current_question(
        self,
    ) -> InterviewQuestion | None:

        if (
            self.current_question_index
            >= self.total_questions
        ):
            return None

        return self.questions[
            self.current_question_index
        ]


# ==========================================================
# Temporary in-memory session store
# ==========================================================

_sessions: dict[str, InterviewSession] = {}


def create_interview_session(
    user_id: int,
    role: str,
    difficulty: str,
    questions: list[InterviewQuestion],
) -> InterviewSession:

    session_id = str(uuid4())

    session = InterviewSession(
        session_id=session_id,
        user_id=user_id,
        role=role,
        difficulty=difficulty,
        questions=questions,
    )

    _sessions[session_id] = session

    return session


def get_interview_session(
    session_id: str,
    user_id: int,
) -> InterviewSession:

    session = _sessions.get(
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found.",
        )

    if session.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this interview.",
        )

    return session


def submit_interview_answer(
    session: InterviewSession,
    answer: str,
) -> InterviewSession:

    if session.status != "active":
        raise HTTPException(
            status_code=400,
            detail="Interview has already been completed.",
        )

    if session.current_question is None:
        raise HTTPException(
            status_code=400,
            detail="There is no active question.",
        )

    session.answers.append(answer)

    session.current_question_index += 1

    if (
        session.current_question_index
        >= session.total_questions
    ):
        session.status = "completed"

    return session


def reset_interview_session(
    session_id: str,
    user_id: int,
) -> InterviewSession:

    session = get_interview_session(
        session_id,
        user_id,
    )

    session.current_question_index = 0
    session.answers = []
    session.status = "active"

    return session