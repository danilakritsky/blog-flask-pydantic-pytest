import os

import pytest

from src.queries import ListArticlesQuery
from src.commands import CreateArticleCommand


@pytest.fixture()
def db():
    os.environ['RUN_ENV'] = 'TEST'
    yield
    del os.environ['RUN_ENV']

@pytest.fixture
def articles():
    articles = []
    for title in ('First post', 'Second post'):
        articles.append(
            CreateArticleCommand(
                author='john@mailbox.com',
                title=title,
                content='Test post')()
        )
    return articles


def test_list_articles_query(articles):
    """
    GIVEN a ListArticlesQuery
    WHEN __call__ method is executed
    THEN a list of all articles stored in the database is returned
    """

    fetched_articles = ListArticlesQuery()
    assert fetched_articles == articles