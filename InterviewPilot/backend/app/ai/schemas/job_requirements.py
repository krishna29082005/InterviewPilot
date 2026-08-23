from pydantic import BaseModel, Field


class JobRequirements(BaseModel):
    required_skills: list[str] = Field(default_factory=list)

    preferred_skills: list[str] = Field(default_factory=list)

    keywords: list[str] = Field(default_factory=list)