import os
import shutil

from fastapi import HTTPException, UploadFile

UPLOAD_DIR = "uploads/resumes"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_resume_filename(user_id: int) -> str:
    return f"{user_id}_resume.pdf"


def get_resume_filepath(user_id: int) -> str | None:
    canonical_path = os.path.join(UPLOAD_DIR, get_resume_filename(user_id))

    if os.path.exists(canonical_path):
        return canonical_path

    matches = [
        os.path.join(UPLOAD_DIR, name)
        for name in os.listdir(UPLOAD_DIR)
        if name.startswith(f"{user_id}_") and name.lower().endswith(".pdf")
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

    filepath = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    # Save (overwrite if already exists)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return {
        "message": "Resume uploaded successfully.",
        "filename": filename,
    }