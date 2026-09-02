import logging
import re

from app.ai.exceptions import AIError
from app.ai.prompts.ats_prompt import ATS_PROMPT
from app.ai.providers.factory import ProviderFactory
from app.ai.schemas.ats_schema import ATSAnalysis, RecommendedRole
from app.ai.schemas.resume import ResumeSchema

logger = logging.getLogger(__name__)


def _normalize(value: str) -> str:
    """
    Normalize text for case-insensitive keyword comparison.
    """

    value = value.lower().strip()

    value = re.sub(
        r"[^a-z0-9+#./-]+",
        " ",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value


def _collect_resume_terms(
    resume: ResumeSchema,
) -> set[str]:
    """
    Collect explicitly declared technical skills from
    the structured resume.

    These terms are considered known/present resume terms.
    """

    terms: set[str] = set()

    technical_skills = resume.technical_skills

    terms.update(
        technical_skills.programming_languages or []
    )

    terms.update(
        technical_skills.frameworks or []
    )

    terms.update(
        technical_skills.libraries or []
    )

    terms.update(
        technical_skills.databases or []
    )

    terms.update(
        technical_skills.cloud or []
    )

    terms.update(
        technical_skills.tools or []
    )

    terms.update(
        technical_skills.technologies or []
    )

    terms.update(
        technical_skills.ai_ml or []
    )

    terms.update(
        technical_skills.gen_ai or []
    )

    # Project technologies are also explicit evidence.
    for project in resume.projects:
        terms.update(
            project.technologies or []
        )

    return {
        _normalize(term)
        for term in terms
        if _normalize(term)
    }


def _build_resume_text(
    resume: ResumeSchema,
) -> str:
    """
    Build searchable text from the structured resume.

    This is used to verify whether Gemini incorrectly
    identifies an existing resume term as missing.
    """

    parts: list[str] = []

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    if resume.summary:
        parts.append(
            resume.summary
        )

    # ------------------------------------------------------
    # Technical skills
    # ------------------------------------------------------

    technical_skills = resume.technical_skills

    parts.extend(
        technical_skills.programming_languages or []
    )

    parts.extend(
        technical_skills.frameworks or []
    )

    parts.extend(
        technical_skills.libraries or []
    )

    parts.extend(
        technical_skills.databases or []
    )

    parts.extend(
        technical_skills.cloud or []
    )

    parts.extend(
        technical_skills.tools or []
    )

    parts.extend(
        technical_skills.technologies or []
    )

    parts.extend(
        technical_skills.ai_ml or []
    )

    parts.extend(
        technical_skills.gen_ai or []
    )

    # ------------------------------------------------------
    # Experience
    # ------------------------------------------------------

    for experience in resume.experience:
        parts.append(
            experience.company
        )

        parts.append(
            experience.title
        )

        parts.extend(
            experience.description
        )

    # ------------------------------------------------------
    # Projects
    # ------------------------------------------------------

    for project in resume.projects:
        parts.append(
            project.title
        )

        if project.description:
            parts.append(
                project.description
            )

        parts.extend(
            project.technologies
        )

        parts.extend(
            project.bullet_points
        )

    # ------------------------------------------------------
    # Additional information
    # ------------------------------------------------------

    parts.extend(
        resume.soft_skills
    )

    parts.extend(
        resume.certifications
    )

    parts.extend(
        resume.achievements
    )

    parts.extend(
        resume.languages
    )

    return _normalize(
        " ".join(parts)
    )


def _filter_missing_keywords(
    resume: ResumeSchema,
    missing_keywords: list[str],
) -> list[str]:
    """
    Validate Gemini's missing-keyword suggestions against
    the actual structured resume.

    If Gemini says a keyword is missing but it already
    appears in the resume, remove it.
    """

    if not missing_keywords:
        return []

    resume_terms = _collect_resume_terms(
        resume
    )

    resume_text = _build_resume_text(
        resume
    )

    validated_missing: list[str] = []
    seen: set[str] = set()

    for keyword in missing_keywords:

        normalized_keyword = _normalize(
            keyword
        )

        if not normalized_keyword:
            continue

        if normalized_keyword in seen:
            continue

        seen.add(
            normalized_keyword
        )

        # Explicit technical skill.
        if normalized_keyword in resume_terms:
            continue

        # Appears somewhere else in the resume.
        if normalized_keyword in resume_text:
            continue

        validated_missing.append(
            keyword
        )

    return validated_missing


def _build_fallback_roles(
    resume: ResumeSchema,
) -> list[RecommendedRole]:
    """
    Generate deterministic role recommendations when
    Gemini is unavailable.

    Recommendations are based only on skills explicitly
    present in the structured resume.
    """

    technical_skills = resume.technical_skills

    # Build normalized skill set.
    skills: set[str] = set()

    skill_groups = [
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

    for group in skill_groups:
        for skill in group or []:
            normalized = _normalize(skill)

            if normalized:
                skills.add(normalized)

    # Also include project technologies.
    for project in resume.projects:
        for technology in project.technologies:
            normalized = _normalize(
                technology
            )

            if normalized:
                skills.add(normalized)

    recommended_roles: list[RecommendedRole] = []

    # ======================================================
    # AI / ML Engineer
    # ======================================================

    ai_ml_signals = {
        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "scikit-learn",
        "computer vision",
        "nlp",
        "natural language processing",
        "llm",
        "generative ai",
        "gen ai",
    }

    ai_matches = [
        skill
        for skill in ai_ml_signals
        if skill in skills
    ]

    if len(ai_matches) >= 2:
        level = "High"
    elif len(ai_matches) == 1:
        level = "Medium"
    else:
        level = None

    if level:
        recommended_roles.append(
            RecommendedRole(
                role="AI/ML Engineer",
                match_level=level,
                reasons=[
                    f"Resume demonstrates {skill}."
                    for skill in ai_matches[:3]
                ],
            )
        )

    # ======================================================
    # Backend Engineer
    # ======================================================

    backend_signals = {
        "python",
        "fastapi",
        "django",
        "flask",
        "node.js",
        "node",
        "rest",
        "rest api",
        "api",
        "postgresql",
        "mysql",
        "mongodb",
        "docker",
    }

    backend_matches = [
        skill
        for skill in backend_signals
        if skill in skills
    ]

    if len(backend_matches) >= 3:
        level = "High"
    elif len(backend_matches) >= 1:
        level = "Medium"
    else:
        level = None

    if level:
        recommended_roles.append(
            RecommendedRole(
                role="Backend Engineer",
                match_level=level,
                reasons=[
                    f"Resume demonstrates {skill}."
                    for skill in backend_matches[:4]
                ],
            )
        )

    # ======================================================
    # Frontend Engineer
    # ======================================================

    frontend_signals = {
        "react",
        "next.js",
        "javascript",
        "typescript",
        "html",
        "css",
        "tailwind",
    }

    frontend_matches = [
        skill
        for skill in frontend_signals
        if skill in skills
    ]

    if len(frontend_matches) >= 3:
        level = "High"
    elif len(frontend_matches) >= 1:
        level = "Medium"
    else:
        level = None

    if level:
        recommended_roles.append(
            RecommendedRole(
                role="Frontend Engineer",
                match_level=level,
                reasons=[
                    f"Resume demonstrates {skill}."
                    for skill in frontend_matches[:4]
                ],
            )
        )

    # ======================================================
    # Data Scientist
    # ======================================================

    data_science_signals = {
        "python",
        "numpy",
        "pandas",
        "scikit-learn",
        "machine learning",
        "statistics",
        "sql",
        "matplotlib",
        "seaborn",
    }

    data_matches = [
        skill
        for skill in data_science_signals
        if skill in skills
    ]

    if len(data_matches) >= 4:
        level = "High"
    elif len(data_matches) >= 2:
        level = "Medium"
    else:
        level = None

    if level:
        recommended_roles.append(
            RecommendedRole(
                role="Data Scientist",
                match_level=level,
                reasons=[
                    f"Resume demonstrates {skill}."
                    for skill in data_matches[:4]
                ],
            )
        )

    # ======================================================
    # DevOps / Cloud Engineer
    # ======================================================

    devops_signals = {
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "google cloud",
        "ci/cd",
        "linux",
    }

    devops_matches = [
        skill
        for skill in devops_signals
        if skill in skills
    ]

    if len(devops_matches) >= 3:
        level = "High"
    elif len(devops_matches) >= 1:
        level = "Medium"
    else:
        level = None

    if level:
        recommended_roles.append(
            RecommendedRole(
                role="DevOps / Cloud Engineer",
                match_level=level,
                reasons=[
                    f"Resume demonstrates {skill}."
                    for skill in devops_matches[:4]
                ],
            )
        )

    # ======================================================
    # General Software Engineer fallback
    # ======================================================

    if not recommended_roles and skills:
        recommended_roles.append(
            RecommendedRole(
                role="Software Engineer",
                match_level="Medium",
                reasons=[
                    "Resume contains technical skills relevant "
                    "to software development.",
                ],
            )
        )

    return recommended_roles


def _build_fallback_analysis(
    resume: ResumeSchema,
) -> ATSAnalysis:
    """
    Generate a deterministic ATS result when Gemini
    is unavailable.

    Since no target job description is available here,
    missing_keywords remains empty.

    Recommended roles are generated from the actual
    technical skills in the resume.
    """

    technical_skills = resume.technical_skills

    keywords: set[str] = set()

    keywords.update(
        technical_skills.programming_languages or []
    )

    keywords.update(
        technical_skills.frameworks or []
    )

    keywords.update(
        technical_skills.libraries or []
    )

    keywords.update(
        technical_skills.databases or []
    )

    keywords.update(
        technical_skills.cloud or []
    )

    keywords.update(
        technical_skills.tools or []
    )

    keywords.update(
        technical_skills.technologies or []
    )

    keywords.update(
        technical_skills.ai_ml or []
    )

    keywords.update(
        technical_skills.gen_ai or []
    )

    has_projects = (
        len(resume.projects) > 0
    )

    has_experience = (
        len(resume.experience) > 0
    )

    has_education = (
        len(resume.education) > 0
    )

    score = 45

    if has_education:
        score += 10

    if has_experience:
        score += 15

    if has_projects:
        score += 15

    if len(keywords) >= 5:
        score += 10

    score = min(
        score,
        95,
    )

    # ------------------------------------------------------
    # Strengths
    # ------------------------------------------------------

    if keywords:
        strengths = [
            "Resume includes structured sections that are easy to parse.",
            "Relevant technical skills are present.",
        ]
    else:
        strengths = [
            "Resume has a clear structure.",
        ]

    # ------------------------------------------------------
    # Weaknesses
    # ------------------------------------------------------

    weaknesses = [
        "Some sections may benefit from stronger keyword targeting.",
        "Quantified impact could be more visible in experience bullets.",
    ]

    # ------------------------------------------------------
    # Recommended roles
    # ------------------------------------------------------

    recommended_roles = _build_fallback_roles(
        resume
    )

    return ATSAnalysis(
        ats_score=score,
        summary=(
            "Fallback ATS analysis generated because "
            "Gemini was unavailable."
        ),
        strengths=strengths,
        weaknesses=weaknesses,
        missing_keywords=[],
        formatting_issues=[],
        improvement_suggestions=[
            "Tailor the summary to the role you are applying for.",
            "Add measurable outcomes to projects and experience bullets.",
            "Mirror key terms from the target job description.",
        ],
        recommended_roles=recommended_roles,
    )


async def generate_ats_analysis(
    resume: ResumeSchema,
) -> ATSAnalysis:
    """
    Generate ATS analysis for a parsed resume.

    Gemini is attempted first.

    If Gemini succeeds:
        - use Gemini's qualitative analysis
        - validate missing keywords against ResumeSchema
        - preserve recommended roles from Gemini

    If Gemini fails:
        - use deterministic ATS fallback
        - generate role recommendations locally
    """

    logger.info(
        "Generating ATS analysis..."
    )

    resume_json = resume.model_dump_json(
        indent=2
    )

    prompt = f"""
{ATS_PROMPT}

Resume:

{resume_json}
"""

    provider = ProviderFactory.get_provider(
        "gemini"
    )

    # ======================================================
    # Gemini-first path
    # ======================================================

    try:

        ats_analysis = await provider.generate(
            prompt=prompt,
            response_model=ATSAnalysis,
        )

        # --------------------------------------------------
        # Validate missing keywords against actual resume.
        # --------------------------------------------------

        validated_missing_keywords = (
            _filter_missing_keywords(
                resume,
                ats_analysis.missing_keywords,
            )
        )

        # --------------------------------------------------
        # Preserve Gemini's recommended roles.
        #
        # We only validate the objective keyword field here.
        # The role recommendations are based on the complete
        # resume and are explicitly requested by the prompt.
        # --------------------------------------------------

        ats_analysis = ats_analysis.model_copy(
            update={
                "missing_keywords": (
                    validated_missing_keywords
                )
            }
        )

        logger.info(
            "ATS analysis generated successfully."
        )

        return ats_analysis

    # ======================================================
    # Gemini failure -> deterministic fallback
    # ======================================================

    except AIError as exc:

        logger.warning(
            "Gemini ATS generation failed, "
            "using fallback: %s",
            exc,
        )

        return _build_fallback_analysis(
            resume
        )