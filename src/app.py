from crypt import methods
from urllib import request
from flask import Flask, jsonify, request

from src.commands import CreateArticleCommand
from src.queries import GetArticleByIdQuery, ListArticlesQuery

app = Flask(__name__)

@app.route('/articles/', methods=["POST"])
def create_article():
    article = CreateArticleCommand(**request.json)()
    # return the dict representation of an object to convert to JSON
    return jsonify(article.dict())
