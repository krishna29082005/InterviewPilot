import logging

from fastapi import APIRouter, Depends, HTTPException

from app.ai.schemas.job_match import JobMatchAnalysis
from app.ai.schemas.job_match_request import JobMatchRequest
from app.ai.schemas.resume import ResumeSchema
from app.ai.services.job_match import extract_job_requirements
from app.api.dependencies.auth import get_current_user
from app.services.job_match import match_resume_to_job
from app.services.resume import get_resume_analysis

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/job-match",
    tags=["Job Match"],
)


@router.post(
    "/analyze",
    response_model=JobMatchAnalysis,
)
async def analyze_job_match(
    request: JobMatchRequest,
    current_user=Depends(get_current_user),
):
    """
    Analyze how well the authenticated user's resume
    matches the supplied job description.
    """

    # ------------------------------------------------------
    # 1. Load the user's existing resume analysis
    # ------------------------------------------------------

    analysis = get_resume_analysis(current_user.id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Resume analysis not found. "
                "Please upload a resume first."
            ),
        )

    try:
        # --------------------------------------------------
        # 2. Convert stored JSON into ResumeSchema
        # --------------------------------------------------

        resume = ResumeSchema.model_validate(analysis)

        # --------------------------------------------------
        # 3. Extract requirements from the JD
        # --------------------------------------------------

        requirements = await extract_job_requirements(
            request.job_description
        )

        # --------------------------------------------------
        # 4. Match resume against requirements
        # --------------------------------------------------

        result = match_resume_to_job(
            resume,
            requirements,
        )

        # --------------------------------------------------
        # 5. Return JobMatchAnalysis
        # --------------------------------------------------

        return result

    except Exception as exc:
        logger.exception(
            "Job matching failed: %s",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to analyze the resume "
                "against the job description."
            ),
        ) from exc