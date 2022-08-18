import os

import pytest
from src.models import Article

from src.queries import GetArticleByIdQuery, ListArticlesQuery
from src.commands import CreateArticleCommand


@pytest.fixture()
def db():
    os.environ['RUN_ENV'] = 'TEST'
    yield
    Article.test_db_connection.close()
    del os.environ['RUN_ENV']

@pytest.fixture
def articles(db):
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
    query = ListArticlesQuery()
    fetched_articles = query()
    assert all(article in articles for article in fetched_articles)


def test_get_articles_by_id(articles):
    """
    GIVEN GetArticleByIdQuery
    WHEN __call__ method is called with a valid id
    THEN an article with this id is retrieved from database and returned
    """
    article = GetArticleByIdQuery(id=articles[0].id)()
    assert article == articles[0]
