import re

from app.ai.schemas.job_match import JobMatchAnalysis
from app.ai.schemas.job_requirements import JobRequirements
from app.ai.schemas.resume import ResumeSchema


def _normalize(value: str) -> str:
    """
    Normalize text so comparisons are case-insensitive
    and punctuation differences don't matter.
    """
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9+#./-]+", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value


def _collect_resume_skills(
    resume: ResumeSchema,
) -> list[str]:
    """
    Collect technical skills from the structured resume.

    We also include technologies explicitly mentioned
    inside projects.
    """

    skills: list[str] = []

    technical_skills = resume.technical_skills

    skills.extend(technical_skills.programming_languages)
    skills.extend(technical_skills.frameworks)
    skills.extend(technical_skills.libraries)
    skills.extend(technical_skills.databases)
    skills.extend(technical_skills.cloud)
    skills.extend(technical_skills.tools)
    skills.extend(technical_skills.technologies)
    skills.extend(technical_skills.ai_ml)
    skills.extend(technical_skills.gen_ai)

    # Project technologies are also evidence of skills.
    for project in resume.projects:
        skills.extend(project.technologies)

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
    Check whether a resume skill matches a job requirement.

    Version 1 uses normalized matching and simple
    naming variations.
    """

    resume_normalized = _normalize(resume_skill)
    required_normalized = _normalize(required_skill)

    if not resume_normalized or not required_normalized:
        return False

    # Exact match
    if resume_normalized == required_normalized:
        return True

    # Handle simple singular/plural differences.
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
            matching.append(required_skill)
        else:
            missing.append(required_skill)

    return matching, missing


def _match_keywords(
    resume: ResumeSchema,
    keywords: list[str],
) -> tuple[list[str], list[str]]:
    """
    Search important job-description keywords across
    the structured resume.
    """

    resume_parts: list[str] = []

    # Resume summary
    if resume.summary:
        resume_parts.append(resume.summary)

    # Experience
    for experience in resume.experience:
        resume_parts.append(experience.company)
        resume_parts.append(experience.title)
        resume_parts.extend(experience.description)

    # Projects
    for project in resume.projects:
        resume_parts.append(project.title)

        if project.description:
            resume_parts.append(project.description)

        resume_parts.extend(project.technologies)
        resume_parts.extend(project.bullet_points)

    # Other resume information
    resume_parts.extend(resume.soft_skills)
    resume_parts.extend(resume.certifications)
    resume_parts.extend(resume.achievements)
    resume_parts.extend(resume.languages)

    resume_text = _normalize(
        " ".join(resume_parts)
    )

    matching: list[str] = []
    missing: list[str] = []

    for keyword in keywords:
        normalized_keyword = _normalize(keyword)

        if not normalized_keyword:
            continue

        if normalized_keyword in resume_text:
            matching.append(keyword)
        else:
            missing.append(keyword)

    return matching, missing


def _calculate_match_score(
    matching_skills: list[str],
    required_skills: list[str],
    matching_keywords: list[str],
    keywords: list[str],
) -> int:
    """
    Calculate the deterministic baseline match score.

    Required skills contribute 70%.
    General keywords contribute 30%.
    """

    if required_skills:
        skill_score = (
            len(matching_skills)
            / len(required_skills)
        ) * 70
    else:
        skill_score = 70

    if keywords:
        keyword_score = (
            len(matching_keywords)
            / len(keywords)
        ) * 30
    else:
        keyword_score = 30

    return round(skill_score + keyword_score)


def match_resume_to_job(
    resume: ResumeSchema,
    requirements: JobRequirements,
) -> JobMatchAnalysis:
    """
    Compare a structured resume against extracted
    job requirements.

    This is the deterministic baseline matcher and
    does not depend on Gemini.
    """

    # ------------------------------------------------------
    # 1. Collect resume skills
    # ------------------------------------------------------

    resume_skills = _collect_resume_skills(resume)

    # ------------------------------------------------------
    # 2. Match required skills
    # ------------------------------------------------------

    matching_skills, missing_skills = _match_skills(
        resume_skills,
        requirements.required_skills,
    )

    # ------------------------------------------------------
    # 3. Match important JD keywords
    # ------------------------------------------------------

    matching_keywords, missing_keywords = _match_keywords(
        resume,
        requirements.keywords,
    )

    # ------------------------------------------------------
    # 4. Calculate baseline score
    # ------------------------------------------------------

    match_score = _calculate_match_score(
        matching_skills,
        requirements.required_skills,
        matching_keywords,
        requirements.keywords,
    )

    # ------------------------------------------------------
    # 5. Check preferred skills
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # 6. Generate strengths
    # ------------------------------------------------------

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
            "The candidate has project experience that supports the application."
        )

    if resume.experience:
        strengths.append(
            "The resume contains professional or organizational experience."
        )

    if not strengths:
        strengths.append(
            "The resume was successfully analyzed against the job description."
        )

    # ------------------------------------------------------
    # 7. Generate gaps
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # 8. Generate recommendations
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # 9. Generate summary
    # ------------------------------------------------------

    summary = (
        f"The resume has a baseline match score of "
        f"{match_score}% based on required skills "
        f"and job-specific keywords."
    )

    # ------------------------------------------------------
    # 10. Return validated Pydantic response
    # ------------------------------------------------------

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