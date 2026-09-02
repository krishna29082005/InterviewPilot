import json
import logging
import shutil
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.ai.exceptions import AIError
from app.ai.services.ai_resume import process_resume

logger = logging.getLogger(__name__)

BACKEND_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BACKEND_ROOT / "uploads" / "resumes"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_resume_filename(user_id: int) -> str:
    return f"{user_id}_resume.pdf"


def get_resume_filepath(user_id: int) -> str | None:
    canonical_path = UPLOAD_DIR / get_resume_filename(user_id)

    if canonical_path.exists():
        return str(canonical_path.resolve())

    matches = [
        str(path.resolve())
        for path in UPLOAD_DIR.glob(f"{user_id}_*.pdf")
    ]

    if matches:
        return sorted(matches)[0]

    return None


async def upload_resume(
    file: UploadFile,
    current_user,
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    filename = get_resume_filename(current_user.id)

    filepath = UPLOAD_DIR / filename
    ats_analysis_path = UPLOAD_DIR / f"{current_user.id}_ats_analysis.json"

    if ats_analysis_path.exists():
        try:
            ats_analysis_path.unlink()
        except OSError:
            logger.warning(
                "Unable to remove previous ATS analysis for user %s.",
                current_user.id,
            )

    with filepath.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    saved_path = str(filepath.resolve())

    logger.info(
        "Resume uploaded successfully for user %s.",
        current_user.id,
    )

    analysis_data = None
    analysis_path = UPLOAD_DIR / f"{current_user.id}_analysis.json"

    try:
        analysis = await process_resume(saved_path)

        if hasattr(analysis, "model_dump"):
            analysis_data = analysis.model_dump()
        else:
            analysis_data = analysis

        with analysis_path.open("w", encoding="utf-8") as file_handle:
            json.dump(
                analysis_data,
                file_handle,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(
            "Resume analysis completed for user %s.",
            current_user.id,
        )

    except AIError:
        logger.warning(
            "AI resume processing failed for user %s; continuing upload.",
            current_user.id,
        )
        analysis_data = None

        if analysis_path.exists():
            try:
                analysis_path.unlink()
            except OSError:
                logger.warning(
                    "Unable to remove incomplete resume analysis for user %s.",
                    current_user.id,
                )

    return {
        "message": "Resume uploaded successfully.",
        "filename": filename,
        "analysis": analysis_data,
    }


def get_resume_analysis(user_id: int):
    path = UPLOAD_DIR / f"{user_id}_analysis.json"

    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_resume_analysis(user_id: int, analysis_data: dict):
    path = UPLOAD_DIR / f"{user_id}_analysis.json"

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            analysis_data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def get_ats_analysis(user_id: int):
    path = UPLOAD_DIR / f"{user_id}_ats_analysis.json"

    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_ats_analysis(user_id: int, ats_data: dict):
    path = UPLOAD_DIR / f"{user_id}_ats_analysis.json"

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            ats_data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def delete_ats_analysis(user_id: int):
    path = UPLOAD_DIR / f"{user_id}_ats_analysis.json"

    if path.exists():
        try:
            path.unlink()
        except OSError:
            logger.warning(
                "Unable to delete ATS analysis for user %s.",
                user_id,
            )