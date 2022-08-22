from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from pydantic import ValidationError

from src.commands import CreateArticleCommand
from src.models import Article
from src.queries import GetArticleByIdQuery, ListArticlesQuery

load_dotenv()

app = Flask(__name__)


@app.errorhandler(ValidationError)
def handle_validation_error(error) -> Response:
    response: Response = jsonify(error.errors())
    response.status_code = 400
    return response


@app.route("/articles/", methods=["GET", "POST"])
def create_article() -> Response:
    if request.method == "POST":
        article: Article = CreateArticleCommand(**request.json)()
        # return the dict representation of an object to convert to JSON
        return jsonify(article.dict())
    if request.method == "GET":
        articles_query: ListArticlesQuery = ListArticlesQuery()
        articles: list[Article] = articles_query()
        return jsonify([article.dict() for article in articles])


@app.route("/articles/<article_id>/", methods=["GET"])
def get_article(article_id: str) -> Response:
    article: Article = GetArticleByIdQuery(id=article_id)()
    # return the dict representation of an object to convert to JSON
    return jsonify(article.dict())


if __name__ == "__main__":
    app.run()
