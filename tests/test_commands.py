import os

import pytest

from src.commands import CreateArticleCommand
from src.models import Article

import ipdb


@pytest.fixture
def db():
    os.environ["RUN_ENV"] = "TEST"
    yield
    del os.environ["RUN_ENV"]


def test_create_article(db):
    """
    GIVEN CreateArticleCommand instance with valid attributes
    WHEN __call__ method called
    THEN a new Article is created with these attributes, saved to a database
    and returned
    """

    create_article_cmd = CreateArticleCommand(
        author="username@mail.com",
        title="new article",
        content="this is my new article",
    )
    
    article = create_article_cmd()

    assert isinstance(article, Article)

    for attr_name in create_article_cmd.__dict__:
        assert getattr(article, attr_name) == getattr(
            create_article_cmd, attr_name
        )
    
    stored_article = Article.get_by_id(article.id)

    assert article == stored_article
