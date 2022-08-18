"""Contains queries, a CQRS pattern objects that
are responsible for reading data from databases."""
from unittest.mock import Base
from pydantic import BaseModel
from .models import Article

import sqlite3

class ListArticlesQuery(BaseModel):
    def __call__(self) -> list[Article]:
        articles: list[Article] = Article.get_all()
        return articles


class GetArticleByIdQuery(Base):
    pass