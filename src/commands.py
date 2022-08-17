from pydantic import BaseModel, EmailStr

class CreateArticleCommand(BaseModel):
    author: EmailStr
    title: str
    content: str