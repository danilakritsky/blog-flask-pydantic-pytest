import json
import pathlib
import sqlite3
import os
from urllib import response

import pytest
import jsonschema

from src.app import app
from src.models import Article



SCHEMAS_DIR = pathlib.Path(__file__).parent / 'schemas'


def validate_payload(payload, schema_name):
    schema = json.load(open(SCHEMAS_DIR / schema_name))
    jsonschema.validate(
        payload,
        schema,
        resolver=jsonschema.RefResolver(
            base_uri=f'file://{SCHEMAS_DIR / schema_name}',
            referrer=schema
        )
    )


@pytest.fixture()
def db():
    os.environ["RUN_ENV"] = "TEST"
    con = sqlite3.connect(
        os.getenv("TEST_DB_PATH") or "file::memory:?cache=shared"
    )
    yield
    con.close()
    del os.environ["RUN_ENV"]


@pytest.fixture
def client(db):
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_create_article(client):
    """
    GIVEN data for a new article
    WHEN POST is called on the /articles/ endpoint
    THEN a new article is returned as a JSON that matches its schema
    """
    article = {
        "author": "john@doe.com",
        "title": "New Article",
        "content": "This is a new article"
    }

    response = client.post(
        '/articles/',
        data=json.dumps(article),
        content_type="application/json")
    validate_payload(response.json, 'Article.json')

def test_get_article(client):
    """
    GIVEN an article id
    WHEN GET is called on the /articles/<article_id>/ endpoint
    THEN an articles with the given id is returned
    """
    article = Article(**{
        "author": "john@doe.com",
        "title": "New Article",
        "content": "This is a new article"
    })
    article.save()
    response = client.get(
        f'/articles/{article.id}/',
        content_type='application/json'
    )
    validate_payload(response.json, 'Article.json')

def test_list_articles(client):
    """
    GIVEN articles stored in a database
    WHEN GET is  callend on the /articles/ endpoint
    THEN an article list is retrieved and returned
    """
    for title in ('First Article', 'Second Article'):
        Article(**{
            "author": "john@doe.com",
            "title": title,
            "content": "This is a new article"
        }).save()

    response = client.get(
        '/articles/',
        content_type='application/json'
    )
    validate_payload(response.json, 'ArticleList.json')

@pytest.mark.parametrize(
    "data",
    [
        {
            "author": "John Doe",
            "title": "New Article",
            "content": "Some extra awesome content"
        },
        {
            "author": "John Doe",
            "title": "New Article",
        },
        {
            "author": "John Doe",
            "title": None,
            "content": "Some extra awesome content"
        }
    ]
)
def test_create_article_bad_request(client, data):
    """
    GIVEN payload with missing/incorrect fields
    WHEN POST request is made against the /articles/ endpoint
    THEN a 400 status is returned with a message detailing the error 
    """
    response = client.post(
        '/articles/',
        data=json.dumps(data),
        content_type='application/json'
    )
    print(response.json)
    assert response.status_code == 400
    assert response.json is not None