import logging

from app.ai.exceptions import AIError
from app.ai.prompts.ats_prompt import ATS_PROMPT
from app.ai.providers.factory import ProviderFactory
from app.ai.schemas.ats_schema import ATSAnalysis
from app.ai.schemas.resume import ResumeSchema

logger = logging.getLogger(__name__)


async def generate_ats_analysis(
    resume: ResumeSchema,
) -> ATSAnalysis:
    """
    Generate ATS analysis for a parsed resume.
    """

    logger.info("Generating ATS analysis...")

    resume_json = resume.model_dump_json(indent=2)

    prompt = f"""
{ATS_PROMPT}

Resume:

{resume_json}
"""

    provider = ProviderFactory.get_provider("gemini")

    try:
        ats_analysis = await provider.generate(
            prompt=prompt,
            response_model=ATSAnalysis,
        )
        logger.info("ATS analysis generated successfully.")
        return ats_analysis

    except AIError as exc:
        logger.warning("Gemini ATS generation failed, using fallback: %s", exc)
        print("⚠️ Gemini ATS generation failed, using fallback ATS analysis.")

    keywords = {
        *(resume.technical_skills.programming_languages or []),
        *(resume.technical_skills.frameworks or []),
        *(resume.technical_skills.libraries or []),
        *(resume.technical_skills.databases or []),
        *(resume.technical_skills.tools or []),
    }

    has_projects = len(resume.projects) > 0
    has_experience = len(resume.experience) > 0
    has_education = len(resume.education) > 0

    score = 45

    if has_education:
        score += 10
    if has_experience:
        score += 15
    if has_projects:
        score += 15
    if len(keywords) >= 5:
        score += 10

    score = min(score, 95)

    return ATSAnalysis(
        ats_score=score,
        summary="Fallback ATS analysis generated because Gemini was unavailable.",
        strengths=[
            "Resume includes structured sections that are easy to parse.",
            "Relevant technical skills are present.",
        ]
        if keywords
        else [
            "Resume has a clear structure.",
        ],
        weaknesses=[
            "Some sections may benefit from stronger keyword targeting.",
            "Quantified impact could be more visible in experience bullets.",
        ],
        missing_keywords=sorted(list(keywords))[:8]
        if keywords
        else [
            "Add job-specific keywords from the target role description.",
        ],
        formatting_issues=[],
        recommendations=[
            "Tailor the summary to the role you are applying for.",
            "Add measurable outcomes to projects and experience bullets.",
            "Mirror key terms from the target job description.",
        ],
    )
