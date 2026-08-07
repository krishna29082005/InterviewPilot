from pydantic import BaseModel

class ATSAnalysis(BaseModel):
    ats_score: int
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    missing_keywords: list[str]
    formatting_issues: list[str]
    improvement_suggestions: list[str]