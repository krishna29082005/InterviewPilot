import logging

from app.ai.exceptions import AIError
from app.ai.parsers.fallback_job_match import (
    extract_job_requirements_fallback,
)
from app.ai.prompts.job_match_prompt import JOB_REQUIREMENTS_PROMPT
from app.ai.providers.factory import ProviderFactory
from app.ai.schemas.job_requirements import JobRequirements

logger = logging.getLogger(__name__)


async def extract_job_requirements(
    job_description: str,
) -> JobRequirements:
    """
    Extract structured requirements from a job description.

    Gemini is attempted first. If Gemini fails, the deterministic
    fallback parser is used.
    """

    logger.info("Extracting job requirements...")

    prompt = f"""
{JOB_REQUIREMENTS_PROMPT}

Job Description:

{job_description}
"""

    provider = ProviderFactory.get_provider("gemini")

    try:
        requirements = await provider.generate(
            prompt=prompt,
            response_model=JobRequirements,
        )

        logger.info(
            "Job requirements extracted successfully."
        )

        return requirements

    except AIError as exc:
        logger.warning(
            "Gemini job requirement extraction failed, "
            "using fallback parser: %s",
            exc,
        )

        return extract_job_requirements_fallback(
            job_description
        )