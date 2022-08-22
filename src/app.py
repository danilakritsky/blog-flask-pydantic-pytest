from crypt import methods
from urllib import request
from pydantic import ValidationError
from flask import Flask, jsonify, request

from dotenv import load_dotenv

from src.commands import CreateArticleCommand
from src.queries import GetArticleByIdQuery, ListArticlesQuery

load_dotenv()

app = Flask(__name__)

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.errors())
    response.status_code = 400
    return response


@app.route('/articles/', methods=["GET", "POST"])
def create_article():
    if request.method == 'POST':
        article = CreateArticleCommand(**request.json)()
        # return the dict representation of an object to convert to JSON
        return jsonify(article.dict())
    if request.method == 'GET':
        articles_query = ListArticlesQuery()
        articles = articles_query()
        return jsonify([article.dict() for article in articles])

@app.route('/articles/<article_id>/', methods=["GET"])
def get_article(article_id):
    article = GetArticleByIdQuery(id=article_id)()
    # return the dict representation of an object to convert to JSON
    return jsonify(article.dict())

if __name__ == "__main__":
    app.run()