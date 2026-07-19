import asyncio
import io
from pathlib import Path

from backend.app.ai.services import resume as resume_service


class FakeUploadFile:
    def __init__(self, filename: str = "myresume.pdf", content: bytes = b"%PDF-1.4"):
        self.filename = filename
        self.content_type = "application/pdf"
        self.file = io.BytesIO(content)


class FakeUser:
    def __init__(self, user_id: int = 9):
        self.id = user_id


def test_upload_resume_uses_canonical_filename(monkeypatch, tmp_path):
    monkeypatch.setattr(resume_service, "UPLOAD_DIR", str(tmp_path))

    result = asyncio.run(resume_service.upload_resume(FakeUploadFile(), FakeUser()))

    assert result["filename"] == "9_resume.pdf"
    assert (tmp_path / "9_resume.pdf").exists()
