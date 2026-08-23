from pydantic import BaseModel


class RecommendedRole(BaseModel):
    role: str
    match_level: str
    reasons: list[str]


class ATSAnalysis(BaseModel):

    ats_score: int

    summary: str

    strengths: list[str]

    weaknesses: list[str]

    missing_keywords: list[str]

    formatting_issues: list[str]

    improvement_suggestions: list[str]

    recommended_roles: list[RecommendedRole]