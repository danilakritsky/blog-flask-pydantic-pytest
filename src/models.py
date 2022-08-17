import uuid

from pydantic import BaseModel, EmailStr, Field


class Article(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: EmailStr
    title: str
    content: str
