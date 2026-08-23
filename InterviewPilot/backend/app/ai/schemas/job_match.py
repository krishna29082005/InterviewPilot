from pydantic import BaseModel, Field


class JobMatchAnalysis(BaseModel):
    match_score: int = Field(ge=0, le=100)

    summary: str

    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)

    matching_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)

    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)