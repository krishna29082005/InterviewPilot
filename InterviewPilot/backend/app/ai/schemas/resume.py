from pydantic import BaseModel, Field, AliasChoices


# ==========================================================
# Personal Information
# ==========================================================

class PersonalInfo(BaseModel):
    full_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("full_name", "name")
    )

    email: str | None = None
    phone: str | None = None
    location: str | None = None

    linkedin: str | None = None
    github: str | None = None
    leetcode: str | None = None
    portfolio: str | None = None


# ==========================================================
# Education
# ==========================================================

class Education(BaseModel):
    institution: str

    degree: str

    field_of_study: str | None = Field(
        default=None,
        validation_alias=AliasChoices("field_of_study", "branch", "specialization")
    )

    start_date: str | None = None

    end_date: str | None = None

    cgpa: str | None = Field(
        default=None,
        validation_alias=AliasChoices("cgpa", "score")
    )


# ==========================================================
# Experience
# ==========================================================

class Experience(BaseModel):

    company: str = Field(
        validation_alias=AliasChoices(
            "company",
            "organization",
            "company_or_organization"
        )
    )

    title: str = Field(
        validation_alias=AliasChoices(
            "title",
            "role",
            "position"
        )
    )

    start_date: str | None = None

    end_date: str | None = None

    location: str | None = None

    description: list[str] = Field(default_factory=list)


# ==========================================================
# Projects
# ==========================================================

class Project(BaseModel):

    title: str

    technologies: list[str] = Field(default_factory=list)

    description: str | None = None

    bullet_points: list[str] = Field(default_factory=list)


# ==========================================================
# Technical Skills
# ==========================================================

class TechnicalSkills(BaseModel):

    programming_languages: list[str] = Field(default_factory=list)

    frameworks: list[str] = Field(default_factory=list)

    libraries: list[str] = Field(default_factory=list)

    databases: list[str] = Field(default_factory=list)

    cloud: list[str] = Field(default_factory=list)

    tools: list[str] = Field(default_factory=list)

    technologies: list[str] = Field(default_factory=list)

    ai_ml: list[str] = Field(default_factory=list)

    gen_ai: list[str] = Field(default_factory=list)


# ==========================================================
# Resume Schema
# ==========================================================

class ResumeSchema(BaseModel):

    personal_info: PersonalInfo

    summary: str | None = None

    education: list[Education] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    technical_skills: TechnicalSkills

    soft_skills: list[str] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)

    achievements: list[str] = Field(default_factory=list)

    languages: list[str] = Field(default_factory=list)