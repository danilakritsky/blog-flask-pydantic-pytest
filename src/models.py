"""Contains our domain models."""

import os
import sqlite3
import uuid
from functools import wraps
from typing import Callable

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field

load_dotenv()


class Article(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    author: EmailStr
    title: str
    content: str

    @staticmethod
    def ensure_table(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            Article.create_table()
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    @ensure_table
    def get_by_id(cls, id: str) -> "Article":
        # not using the context manager since it just commits the transaction,
        # and does note close the connection
        con: sqlite3.Connection = Article.get_connection()
        con.row_factory = sqlite3.Row  # dict rows
        cur: sqlite3.Cursor = con.cursor()
        res: sqlite3.Cursor = cur.execute(
            "SELECT * FROM articles WHERE id = ?", (id,)
        )

        article: Article = cls(**res.fetchone())
        con.close()  # !!! close the connection
        return article

    # classmethod should be preferred over staticmethod
    # if the class is expected to be inherited
    # https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner

    @staticmethod
    def create_table() -> None:
        con: sqlite3.Connection = Article.get_connection()
        with con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS
                articles(id TEXT, author TEXT, title TEXT, content TEXT)
                """
            )

        if os.getenv("RUN_ENV") != "TEST":
            con.close()
        else:
            # if env is TEST keep connection alive for the db to persist
            setattr(Article, "test_db_connection", con)

    @staticmethod
    def _get_db_path() -> str:
        db: str
        if os.getenv("RUN_ENV") == "TEST":
            db = os.getenv("TEST_DB_PATH") or "file::memory:?cache=shared"
        else:
            db = os.getenv("DB_PATH") or "database.db"
        return db

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        con: sqlite3.Connection = sqlite3.connect(
            Article._get_db_path(), uri=True
        )
        return con

    @ensure_table
    def save(self) -> None:
        con: sqlite3.Connection = Article.get_connection()
        with con:
            con.execute(
                """
                INSERT INTO
                articles(id, author, title, content)
                VALUES
                (?, ?, ?, ?)
                """,
                (self.id, self.author, self.title, self.content),
            )
        con.close()

    @classmethod
    @ensure_table
    def get_all(cls) -> list["Article"]:
        con: sqlite3.Connection = Article.get_connection()
        con.row_factory = sqlite3.Row
        with con:
            res: list[Article] = [
                cls(**row) for row in con.execute(
                    """SELECT * FROM articles""",
                )
            ]
        con.close()
        return res
