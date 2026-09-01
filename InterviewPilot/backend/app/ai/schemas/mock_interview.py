from pydantic import BaseModel, Field


class MockInterviewStartRequest(BaseModel):
    role: str = Field(min_length=1)

    difficulty: str = Field(
        default="medium",
        pattern="^(easy|medium|hard)$",
    )

    question_count: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class MockInterviewAnswerRequest(BaseModel):
    answer: str = Field(
        min_length=1,
    )


class InterviewQuestion(BaseModel):
    id: int
    question: str
    category: str
    difficulty: str


class InterviewQuestions(BaseModel):
    questions: list[InterviewQuestion] = Field(
        default_factory=list
    )


class MockInterviewResponse(BaseModel):
    session_id: str
    role: str
    difficulty: str
    question_number: int
    total_questions: int
    question: str | None
    category: str | None
    status: str