import json
import pathlib

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


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_create_article(client):
    """
    GIVEN data for a new article
    WHEN post is called on an endpoint
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
