from pydantic import BaseModel, Field


class InterviewEvaluation(BaseModel):
    overall_score: int = Field(
        ge=0,
        le=100,
    )

    technical_score: int = Field(
        ge=0,
        le=100,
    )

    relevance_score: int = Field(
        ge=0,
        le=100,
    )

    communication_score: int = Field(
        ge=0,
        le=100,
    )

    problem_solving_score: int = Field(
        ge=0,
        le=100,
    )

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    improvement_suggestions: list[str] = Field(
        default_factory=list
    )

    summary: str

    question_feedback: list[str] = Field(
        default_factory=list
    )