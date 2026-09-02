import asyncio
import logging
import os
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import ValidationError

from app.ai.exceptions import AIError
from app.api.dependencies.auth import get_current_user
from app.ai.services.ai_resume import process_resume
from app.services.resume import (
    get_resume_analysis,
    get_resume_filepath,
    save_resume_analysis,
    upload_resume,
)

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post("/upload")
async def upload_resume_route(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    return await upload_resume(file, current_user)

@router.get("/info")
def get_resume_info(
    current_user=Depends(get_current_user),
):
    file_path = get_resume_filepath(current_user.id)

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    uploaded_time = datetime.fromtimestamp(
        os.path.getmtime(file_path)
    )

    analysis = get_resume_analysis(current_user.id)

    if analysis is None and file_path:
        try:
            parsed_resume = asyncio.run(process_resume(file_path))
            analysis = parsed_resume.model_dump()
            save_resume_analysis(current_user.id, analysis)
        except (AIError, OSError, ValidationError) as exc:
            logger.warning(
                "Resume analysis could not be regenerated: %s",
                exc,
            )

    return {
        "filename": os.path.basename(file_path),
        "size": os.path.getsize(file_path),
        "uploaded_at": uploaded_time.strftime("%d %b %Y, %I:%M %p"),
        "analysis": analysis,
    }
@router.get("/download")
def download_resume(
    current_user=Depends(get_current_user),
):
    file_path = get_resume_filepath(current_user.id)

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="Resume.pdf",
    )

@router.delete("/delete")
def delete_resume(
    current_user=Depends(get_current_user),
):
    file_path = get_resume_filepath(current_user.id)

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    # Delete PDF
    os.remove(file_path)

    # Delete analysis JSON
    analysis_path = os.path.join(
        os.path.dirname(file_path),
        f"{current_user.id}_analysis.json",
    )

    if os.path.exists(analysis_path):
        os.remove(analysis_path)

    return {
        "message": "Resume deleted successfully."
    }
