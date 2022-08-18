"""Contains queries, a CQRS pattern objects that
are responsible for reading data from databases."""
from pydantic import BaseModel
from .models import Article

class ListArticlesQuery(BaseModel):
    pass