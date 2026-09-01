from typing import Literal

from pydantic import BaseModel, Field


ChatContext = Literal[
    "resume",
    "ats_analysis",
    "job_match",
    "interview",
]


class ChatMessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
    )


class ChatContextSelection(BaseModel):
    contexts: list[ChatContext] = Field(
        default_factory=list,
        min_length=1,
        max_length=4,
    )


class ChatMessageResponse(BaseModel):
    reply: str

    context_used: list[ChatContext] = Field(
        default_factory=list,
    )