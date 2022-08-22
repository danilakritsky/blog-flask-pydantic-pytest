from crypt import methods
from urllib import request
from flask import Flask, jsonify, request

from src.commands import CreateArticleCommand
from src.queries import GetArticleByIdQuery, ListArticlesQuery

app = Flask(__name__)

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

