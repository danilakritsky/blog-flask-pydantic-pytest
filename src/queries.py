"""Contains queries, a CQRS pattern objects that
are responsible for reading data from databases."""

from pydantic import BaseModel

from .models import Article


class ListArticlesQuery(BaseModel):
    def __call__(self) -> list[Article]:
        articles: list[Article] = Article.get_all()
        return articles


class GetArticleByIdQuery(BaseModel):
    id: str

    def __call__(self) -> Article:
        return Article.get_by_id(self.id)
