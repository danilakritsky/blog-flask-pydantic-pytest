"""Contains commands, a CQRS pattern objects that
are responsible for writing data to databases."""


from pydantic import BaseModel, EmailStr

from .models import Article


# commands in CQRS are responsible for writing to the db
class CreateArticleCommand(BaseModel):
    author: EmailStr
    title: str
    content: str

    def __call__(self) -> Article:
        article: Article = Article(
            author=self.author, title=self.title, content=self.content
        )
        article.save()
        return article
