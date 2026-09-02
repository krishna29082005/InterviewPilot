import re
import json
import logging
from pathlib import Path

from pydantic import ValidationError

from app.ai.schemas.job_match import JobMatchAnalysis
from app.ai.schemas.job_requirements import JobRequirements
from app.ai.schemas.resume import ResumeSchema


logger = logging.getLogger(__name__)


def _normalize(value: str) -> str:
    """
    Normalize text so comparisons are case-insensitive
    and punctuation differences do not matter.
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


def _collect_resume_skills(
    resume: ResumeSchema,
) -> list[str]:
    """
    Collect all explicitly declared technical skills
    from the structured resume.

    Project technologies are also included because they
    are evidence of skills demonstrated by the candidate.
    """

    skills: list[str] = []

    technical_skills = resume.technical_skills

    skills.extend(
        technical_skills.programming_languages
    )

    skills.extend(
        technical_skills.frameworks
    )

    skills.extend(
        technical_skills.libraries
    )

    skills.extend(
        technical_skills.databases
    )

    skills.extend(
        technical_skills.cloud
    )

    skills.extend(
        technical_skills.tools
    )

    skills.extend(
        technical_skills.technologies
    )

    skills.extend(
        technical_skills.ai_ml
    )

    skills.extend(
        technical_skills.gen_ai
    )

    # Also include technologies explicitly mentioned
    # inside projects.
    for project in resume.projects:
        skills.extend(
            project.technologies
        )

    # Remove duplicates while preserving order.
    result: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        normalized = _normalize(skill)

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)
        result.append(skill.strip())

    return result


def _skill_matches(
    resume_skill: str,
    required_skill: str,
) -> bool:
    """
    Determine whether a resume skill satisfies
    a job requirement.

    Uses normalized exact matching plus simple
    naming variations.
    """

    resume_normalized = _normalize(
        resume_skill
    )

    required_normalized = _normalize(
        required_skill
    )

    if not resume_normalized or not required_normalized:
        return False

    # Exact match.
    if resume_normalized == required_normalized:
        return True

    # Handle simple plural differences.
    #
    # REST API
    # REST APIs
    #
    if (
        resume_normalized.rstrip("s")
        == required_normalized.rstrip("s")
    ):
        return True

    # Handle simple contained terms.
    return (
        resume_normalized in required_normalized
        or required_normalized in resume_normalized
    )


def _match_skills(
    resume_skills: list[str],
    required_skills: list[str],
) -> tuple[list[str], list[str]]:
    """
    Compare resume skills against required job skills.
    """

    matching: list[str] = []
    missing: list[str] = []

    for required_skill in required_skills:

        found = any(
            _skill_matches(
                resume_skill,
                required_skill,
            )
            for resume_skill in resume_skills
        )

        if found:
            matching.append(
                required_skill
            )
        else:
            missing.append(
                required_skill
            )

    return matching, missing


def _match_keywords(
    resume: ResumeSchema,
    keywords: list[str],
) -> tuple[list[str], list[str]]:
    """
    Search important JD keywords across the complete
    structured resume.

    Technical skills are intentionally included here.

    This prevents inconsistencies such as:

        Docker -> matching skill

    while simultaneously having:

        Docker -> missing keyword

    when Docker is present in ResumeSchema.technical_skills.
    """

    resume_parts: list[str] = []

    # ======================================================
    # Summary
    # ======================================================

    if resume.summary:
        resume_parts.append(
            resume.summary
        )

    # ======================================================
    # Technical Skills
    # ======================================================

    technical_skills = resume.technical_skills

    resume_parts.extend(
        technical_skills.programming_languages
    )

    resume_parts.extend(
        technical_skills.frameworks
    )

    resume_parts.extend(
        technical_skills.libraries
    )

    resume_parts.extend(
        technical_skills.databases
    )

    resume_parts.extend(
        technical_skills.cloud
    )

    resume_parts.extend(
        technical_skills.tools
    )

    resume_parts.extend(
        technical_skills.technologies
    )

    resume_parts.extend(
        technical_skills.ai_ml
    )

    resume_parts.extend(
        technical_skills.gen_ai
    )

    # ======================================================
    # Experience
    # ======================================================

    for experience in resume.experience:

        resume_parts.append(
            experience.company
        )

        resume_parts.append(
            experience.title
        )

        resume_parts.extend(
            experience.description
        )

    # ======================================================
    # Projects
    # ======================================================

    for project in resume.projects:

        resume_parts.append(
            project.title
        )

        if project.description:
            resume_parts.append(
                project.description
            )

        resume_parts.extend(
            project.technologies
        )

        resume_parts.extend(
            project.bullet_points
        )

    # ======================================================
    # Additional Resume Information
    # ======================================================

    resume_parts.extend(
        resume.soft_skills
    )

    resume_parts.extend(
        resume.certifications
    )

    resume_parts.extend(
        resume.achievements
    )

    resume_parts.extend(
        resume.languages
    )

    # ======================================================
    # Normalize complete resume text
    # ======================================================

    resume_text = _normalize(
        " ".join(resume_parts)
    )

    matching: list[str] = []
    missing: list[str] = []

    # ======================================================
    # Compare JD keywords
    # ======================================================

    for keyword in keywords:

        normalized_keyword = _normalize(
            keyword
        )

        if not normalized_keyword:
            continue

        if normalized_keyword in resume_text:
            matching.append(
                keyword
            )
        else:
            missing.append(
                keyword
            )

    return matching, missing


def _calculate_match_score(
    matching_skills: list[str],
    required_skills: list[str],
    matching_keywords: list[str],
    keywords: list[str],
) -> int:
    """
    Calculate a deterministic baseline match score.

    Required skills contribute 70%.
    General job-description keywords contribute 30%.
    """

    # ======================================================
    # Required skill score
    # ======================================================

    if required_skills:

        skill_score = (
            len(matching_skills)
            / len(required_skills)
        ) * 70

    else:

        # If the JD contains no required skills,
        # give the full skill portion.
        skill_score = 70

    # ======================================================
    # Keyword score
    # ======================================================

    if keywords:

        keyword_score = (
            len(matching_keywords)
            / len(keywords)
        ) * 30

    else:

        # If there are no keywords,
        # give the full keyword portion.
        keyword_score = 30

    # ======================================================
    # Final score
    # ======================================================

    score = round(
        skill_score + keyword_score
    )

    # Safety clamp.
    return max(
        0,
        min(score, 100),
    )


def match_resume_to_job(
    resume: ResumeSchema,
    requirements: JobRequirements,
) -> JobMatchAnalysis:
    """
    Compare a structured resume against extracted
    job requirements.

    This is the deterministic baseline matcher.

    It does NOT depend on Gemini and therefore continues
    working even when the Gemini API is unavailable.
    """

    # ======================================================
    # 1. Collect resume skills
    # ======================================================

    resume_skills = _collect_resume_skills(
        resume
    )

    # ======================================================
    # 2. Match required skills
    # ======================================================

    matching_skills, missing_skills = _match_skills(
        resume_skills,
        requirements.required_skills,
    )

    # ======================================================
    # 3. Match JD keywords
    # ======================================================

    matching_keywords, missing_keywords = _match_keywords(
        resume,
        requirements.keywords,
    )

    # ======================================================
    # 4. Calculate match score
    # ======================================================

    match_score = _calculate_match_score(
        matching_skills,
        requirements.required_skills,
        matching_keywords,
        requirements.keywords,
    )

    # ======================================================
    # 5. Check preferred skills
    # ======================================================

    missing_preferred_skills = [
        skill
        for skill in requirements.preferred_skills
        if not any(
            _skill_matches(
                resume_skill,
                skill,
            )
            for resume_skill in resume_skills
        )
    ]

    # ======================================================
    # 6. Generate strengths
    # ======================================================

    strengths: list[str] = []

    if matching_skills:
        strengths.append(
            "The resume contains several skills required by the job."
        )

    if matching_keywords:
        strengths.append(
            "The resume contains relevant keywords from the job description."
        )

    if resume.projects:
        strengths.append(
            "The candidate has project experience that can support the application."
        )

    if resume.experience:
        strengths.append(
            "The resume contains professional or organizational experience."
        )

    if not strengths:
        strengths.append(
            "The resume was successfully analyzed against the job description."
        )

    # ======================================================
    # 7. Generate gaps
    # ======================================================

    gaps: list[str] = []

    if missing_skills:
        gaps.append(
            "Some required technical skills are missing from the resume."
        )

    if missing_keywords:
        gaps.append(
            "Several important job-description keywords are not present."
        )

    if missing_preferred_skills:
        gaps.append(
            "Some preferred skills are not currently demonstrated."
        )

    if not gaps:
        gaps.append(
            "No major skill or keyword gaps were detected by the baseline matcher."
        )

    # ======================================================
    # 8. Generate recommendations
    # ======================================================

    recommendations: list[str] = []

    if missing_skills:
        recommendations.append(
            "Develop and highlight the missing required skills where relevant."
        )

    if missing_keywords:
        recommendations.append(
            "Use relevant job-specific terminology in your resume when it accurately reflects your experience."
        )

    if missing_preferred_skills:
        recommendations.append(
            "Consider gaining or demonstrating experience with the preferred skills."
        )

    if not recommendations:
        recommendations.append(
            "Maintain strong alignment between the resume and the target job description."
        )

    # ======================================================
    # 9. Generate summary
    # ======================================================

    summary = (
        f"The resume has a baseline match score of "
        f"{match_score}% based on required skills "
        f"and job-specific keywords."
    )

    # ======================================================
    # 10. Return validated result
    # ======================================================

    return JobMatchAnalysis(
        match_score=match_score,
        summary=summary,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        matching_keywords=matching_keywords,
        missing_keywords=missing_keywords,
        strengths=strengths,
        gaps=gaps,
        recommendations=recommendations,
    )
JOB_MATCH_DIR = (
    Path(__file__).resolve().parents[2]
    / "uploads"
    / "resumes"
)


def get_job_match_result(
    user_id: int,
) -> dict | None:
    """
    Return the most recently saved job-match result
    for the user.
    """

    path = (
        JOB_MATCH_DIR
        / f"{user_id}_job_match.json"
    )

    if not path.exists():
        return None

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

            if not isinstance(data, dict):
                return None

            analysis = JobMatchAnalysis.model_validate(
                data.get("analysis")
            )

            if not isinstance(data.get("job_description"), str):
                return None

            return {
                "job_description": data["job_description"],
                "analysis": analysis.model_dump(),
            }

    except (OSError, json.JSONDecodeError, ValidationError):
        return None


def save_job_match_result(
    user_id: int,
    job_description: str,
    result: JobMatchAnalysis,
) -> None:
    """
    Save the latest job description and its matching result.
    """

    JOB_MATCH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        JOB_MATCH_DIR
        / f"{user_id}_job_match.json"
    )

    data = {
        "job_description": job_description,
        "analysis": result.model_dump(),
    }

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def delete_job_match_result(user_id: int) -> None:
    """Remove the cached job-match result for the user, if present."""

    path = JOB_MATCH_DIR / f"{user_id}_job_match.json"

    if path.exists():
        try:
            path.unlink()
        except OSError:
            logger.warning(
                "Unable to delete job-match result for user %s.",
                user_id,
            )
