from fastapi import APIRouter, Depends, UploadFile, File
from app.api.dependencies.auth import get_current_user
from app.services.resume import upload_resume, get_resume_filepath
from fastapi import HTTPException
from fastapi.responses import FileResponse


import os
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

    from datetime import datetime

    uploaded_time = datetime.fromtimestamp(
    os.path.getmtime(file_path)
)
    return {
    "filename": os.path.basename(file_path),
    "size": os.path.getsize(file_path),
    "uploaded_at": uploaded_time.strftime("%d %b %Y, %I:%M %p"),
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

    os.remove(file_path)

    return {
        "message": "Resume deleted successfully."
    }