from crypt import methods
from urllib import request
from flask import Flask

from src.commands import CreateArticleCommand
from src.queries import GetArticleByIdQuery, ListArticlesQuery

app = Flask(__name__)

@app.route('/', methods=["POST"])
def create_article():
    pass