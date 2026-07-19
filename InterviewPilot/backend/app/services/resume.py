import os
import shutil
from pathlib import Path
import json
from fastapi import HTTPException, UploadFile
import json
from app.ai.services.ai_resume import process_resume

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
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    # One resume per user
    filename = get_resume_filename(current_user.id)
    
    filepath = UPLOAD_DIR / filename

    # Save (overwrite if already exists)
    with filepath.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    saved_path = str(filepath.resolve())
    print("=" * 60)
    print("Saved path:", saved_path)
    print("File size:", os.path.getsize(saved_path))
    print("=" * 60) 
    # AI Processing
    analysis = await process_resume(saved_path)
    analysis_path = UPLOAD_DIR / f"{current_user.id}_analysis.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
       json.dump(
        analysis.model_dump(),
        f,
        indent=4,
        ensure_ascii=False,
    )

    if hasattr(analysis, "model_dump"):
        analysis_data = analysis.model_dump()
    else:
        analysis_data = analysis

    print("\n========== RESUME ANALYSIS ==========")
    print(analysis_data)
    print("======================================\n")

    return {
        "message": "Resume uploaded successfully.",
        "filename": filename,
        "analysis": analysis_data,
    }
import json

def get_resume_analysis(user_id: int):
    path = UPLOAD_DIR / f"{user_id}_analysis.json"

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)