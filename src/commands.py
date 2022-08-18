from pydantic import BaseModel, EmailStr

from .models import Article


class CreateArticleCommand(BaseModel):
    author: EmailStr
    title: str
    content: str

    def __call__(self):
        return Article(
            author=self.author, title=self.title, content=self.content
        )
