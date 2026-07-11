from pydantic import BaseModel, Field


class ResumeUploadRequest(BaseModel):
    file_name: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class ResumeUploadResponse(BaseModel):
    success: bool
    message: str
    extracted_skills: list[str] = []
