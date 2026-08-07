from fastapi import APIRouter, Depends, HTTPException
import logging

from app.api.dependencies.auth import get_current_user
from app.services.resume import get_resume_analysis, get_resume_filepath
from app.ai.services.ai_resume import process_resume

from app.ai.schemas.resume import ResumeSchema, PersonalInfo, TechnicalSkills
from app.ai.services.ats_service import generate_ats_analysis

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ats",
    tags=["ATS"],
)


@router.get("/analysis")
async def get_ats_analysis(
    current_user=Depends(get_current_user),
):
    analysis = get_resume_analysis(current_user.id)
    resume = None

    if analysis is None:
        file_path = get_resume_filepath(current_user.id)

        if not file_path:
            raise HTTPException(
                status_code=404,
                detail="Resume not found.",
            )

        try:
          parsed_resume = await process_resume(file_path)
          analysis = parsed_resume.model_dump()
        except Exception as exc:
            logger.warning(
                "ATS resume parsing failed, using fallback resume schema: %s",
                exc,
            )
            resume = ResumeSchema(
                personal_info=PersonalInfo(),
                technical_skills=TechnicalSkills(),
            )

    if resume is None:
        resume = ResumeSchema.model_validate(analysis)

    ats = await generate_ats_analysis(resume)

    return ats
