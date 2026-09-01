import logging

from app.ai.exceptions import AIError
from app.ai.providers.factory import ProviderFactory
from app.ai.prompts.mock_interview_prompt import MOCK_INTERVIEW_PROMPT
from app.ai.schemas.mock_interview import (
    InterviewQuestion,
    InterviewQuestions,
)
from app.ai.schemas.resume import ResumeSchema

logger = logging.getLogger(__name__)


def _build_resume_context(
    resume: ResumeSchema,
) -> str:
    """
    Convert the structured ResumeSchema into compact text
    that can be included in the interview-generation prompt.
    """

    parts: list[str] = []

    if resume.summary:
        parts.append(
            f"Summary: {resume.summary}"
        )

    technical_skills = resume.technical_skills

    skill_groups = {
        "Programming Languages": (
            technical_skills.programming_languages
        ),
        "Frameworks": technical_skills.frameworks,
        "Libraries": technical_skills.libraries,
        "Databases": technical_skills.databases,
        "Cloud": technical_skills.cloud,
        "Tools": technical_skills.tools,
        "Technologies": technical_skills.technologies,
        "AI/ML": technical_skills.ai_ml,
        "Generative AI": technical_skills.gen_ai,
    }

    for label, skills in skill_groups.items():
        if skills:
            parts.append(
                f"{label}: {', '.join(skills)}"
            )

    if resume.projects:
        parts.append("\nProjects:")

        for project in resume.projects:
            project_text = [
                project.title,
                *project.technologies,
                *(project.bullet_points or []),
            ]

            if project.description:
                project_text.append(
                    project.description
                )

            parts.append(
                "- " + " | ".join(project_text)
            )

    if resume.experience:
        parts.append("\nExperience:")

        for experience in resume.experience:
            parts.append(
                f"- {experience.title} at "
                f"{experience.company}"
            )

            parts.extend(
                f"  {description}"
                for description in experience.description
            )

    return "\n".join(parts)


def _fallback_questions(
    role: str,
    difficulty: str,
    question_count: int,
    resume: ResumeSchema,
) -> list[InterviewQuestion]:
    """
    Deterministic fallback question generator.

    The fallback uses the target role and technologies present
    in the resume. It does not require Gemini.
    """

    role_normalized = role.lower()

    technical_skills = resume.technical_skills

    skills = {
        skill.lower()
        for group in [
            technical_skills.programming_languages,
            technical_skills.frameworks,
            technical_skills.libraries,
            technical_skills.databases,
            technical_skills.cloud,
            technical_skills.tools,
            technical_skills.technologies,
            technical_skills.ai_ml,
            technical_skills.gen_ai,
        ]
        for skill in group
    }

    questions: list[InterviewQuestion] = []

    # ------------------------------------------------------
    # Backend
    # ------------------------------------------------------

    if (
        "backend" in role_normalized
        or "back-end" in role_normalized
    ):
        questions.extend(
            [
                InterviewQuestion(
                    id=1,
                    question=(
                        "What is a REST API, and what are the "
                        "main HTTP methods commonly used with it?"
                    ),
                    category="Fundamentals",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=2,
                    question=(
                        "Explain the difference between "
                        "authentication and authorization in a backend system."
                    ),
                    category="Technical",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=3,
                    question=(
                        "How would you design a backend API "
                        "that needs to handle many concurrent users?"
                    ),
                    category="System Design",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=4,
                    question=(
                        "An API endpoint has become slow in production. "
                        "How would you investigate the problem?"
                    ),
                    category="Problem Solving",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=5,
                    question=(
                        "What are some important practices for "
                        "securing a REST API?"
                    ),
                    category="Practical",
                    difficulty=difficulty,
                ),
            ]
        )

    # ------------------------------------------------------
    # AI / ML
    # ------------------------------------------------------

    elif (
        "ai" in role_normalized
        or "ml" in role_normalized
        or "machine learning" in role_normalized
        or "artificial intelligence" in role_normalized
    ):
        questions.extend(
            [
                InterviewQuestion(
                    id=1,
                    question=(
                        "What is the difference between "
                        "supervised and unsupervised learning?"
                    ),
                    category="Fundamentals",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=2,
                    question=(
                        "Explain the bias-variance tradeoff "
                        "and how it relates to model generalization."
                    ),
                    category="Technical",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=3,
                    question=(
                        "How would you detect and reduce "
                        "overfitting in a machine learning model?"
                    ),
                    category="Technical",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=4,
                    question=(
                        "How would you design a production "
                        "machine-learning pipeline?"
                    ),
                    category="System Design",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=5,
                    question=(
                        "A model performs well during training "
                        "but poorly in production. How would you debug it?"
                    ),
                    category="Problem Solving",
                    difficulty=difficulty,
                ),
            ]
        )

    # ------------------------------------------------------
    # Data Science
    # ------------------------------------------------------

    elif (
        "data scientist" in role_normalized
        or "data science" in role_normalized
    ):
        questions.extend(
            [
                InterviewQuestion(
                    id=1,
                    question=(
                        "What is the difference between "
                        "correlation and causation?"
                    ),
                    category="Fundamentals",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=2,
                    question=(
                        "Explain precision, recall, and F1 score "
                        "and when you would use each."
                    ),
                    category="Technical",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=3,
                    question=(
                        "How would you handle missing values "
                        "in a real-world dataset?"
                    ),
                    category="Technical",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=4,
                    question=(
                        "How would you design an end-to-end "
                        "machine-learning workflow for a prediction problem?"
                    ),
                    category="System Design",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=5,
                    question=(
                        "How would you determine whether a model "
                        "is actually useful for a business problem?"
                    ),
                    category="Practical",
                    difficulty=difficulty,
                ),
            ]
        )

    # ------------------------------------------------------
    # Frontend
    # ------------------------------------------------------

    elif (
        "frontend" in role_normalized
        or "front-end" in role_normalized
    ):
        questions.extend(
            [
                InterviewQuestion(
                    id=1,
                    question=(
                        "What is the difference between state "
                        "and props in React?"
                    ),
                    category="Fundamentals",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=2,
                    question=(
                        "Explain how React rendering works."
                    ),
                    category="Technical",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=3,
                    question=(
                        "How would you improve the performance "
                        "of a slow React application?"
                    ),
                    category="Problem Solving",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=4,
                    question=(
                        "How would you structure a large "
                        "frontend application?"
                    ),
                    category="System Design",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=5,
                    question=(
                        "How would you design a reusable "
                        "component system for a dashboard?"
                    ),
                    category="Practical",
                    difficulty=difficulty,
                ),
            ]
        )

    # ------------------------------------------------------
    # Generic role fallback
    # ------------------------------------------------------

    else:
        questions.extend(
            [
                InterviewQuestion(
                    id=1,
                    question=(
                        f"What are the most important fundamentals "
                        f"a {role} should understand?"
                    ),
                    category="Fundamentals",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=2,
                    question=(
                        f"Describe an important technical concept "
                        f"commonly used by a {role}."
                    ),
                    category="Technical",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=3,
                    question=(
                        f"How would you approach a difficult "
                        f"technical problem as a {role}?"
                    ),
                    category="Problem Solving",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=4,
                    question=(
                        f"How would you design a production system "
                        f"relevant to a {role}?"
                    ),
                    category="System Design",
                    difficulty=difficulty,
                ),
                InterviewQuestion(
                    id=5,
                    question=(
                        f"Describe a challenging situation a {role} "
                        f"might encounter and how you would debug it."
                    ),
                    category="Practical",
                    difficulty=difficulty,
                ),
            ]
        )

    # ------------------------------------------------------
    # Add one resume-specific question where possible
    # ------------------------------------------------------

    if skills and questions:
        interesting_skill = next(iter(skills))

        questions[-1] = InterviewQuestion(
            id=questions[-1].id,
            question=(
                f"Your resume mentions {interesting_skill}. "
                f"Explain how you have used it and describe one "
                f"technical challenge you faced while working with it."
            ),
            category="Resume-Based",
            difficulty=difficulty,
        )

    return questions[:question_count]


async def generate_interview_questions(
    resume: ResumeSchema,
    role: str,
    difficulty: str,
    question_count: int,
) -> list[InterviewQuestion]:
    """
    Generate mock-interview questions using Gemini first
    and a deterministic fallback if Gemini is unavailable.
    """

    resume_context = _build_resume_context(
        resume
    )

    prompt = f"""
{MOCK_INTERVIEW_PROMPT}

Target Role:
{role}

Difficulty:
{difficulty}

Question Count:
{question_count}

Candidate Resume:

{resume_context}
"""

    provider = ProviderFactory.get_provider(
        "gemini"
    )

    try:
        result = await provider.generate(
            prompt=prompt,
            response_model=InterviewQuestions,
        )

        questions = result.questions[:question_count]

        if not questions:
            raise AIError(
                "Gemini returned no interview questions."
            )

        logger.info(
            "Generated %d mock interview questions using Gemini.",
            len(questions),
        )

        return questions

    except AIError as exc:
        logger.warning(
            "Gemini mock interview generation failed, "
            "using deterministic fallback: %s",
            exc,
        )

        return _fallback_questions(
            role=role,
            difficulty=difficulty,
            question_count=question_count,
            resume=resume,
        )