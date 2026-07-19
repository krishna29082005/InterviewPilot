import asyncio
import io
from types import SimpleNamespace

from fastapi import UploadFile

from app.services.resume import upload_resume


class DummyFile:
    def __init__(self):
        self.file = io.BytesIO(b'%PDF-1.4\n%test')
        self.content_type = 'application/pdf'

    async def read(self):
        return b''

    async def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration


dummy = UploadFile(file=DummyFile().file, filename='sample.pdf')
current_user = SimpleNamespace(id=123)
print(asyncio.run(upload_resume(dummy, current_user)))
