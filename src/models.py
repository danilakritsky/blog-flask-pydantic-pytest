"""Contains domain models."""

import os
import sqlite3
import uuid
from functools import wraps
from typing import Callable
from sqlite3 import Cursor, Connection, Row

from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, Field

load_dotenv()


def get_db_path() -> str:
    db: str
    if os.getenv("RUN_ENV") == "TEST":
        db = os.getenv("TEST_DB_PATH") or "file::memory:?cache=shared"
    else:
        db = os.getenv("DB_PATH") or "database.db"
    return db


def get_connection() -> Connection:
    con: Connection = sqlite3.connect(get_db_path(), uri=True)
    con.row_factory: Row = sqlite3.Row  # dict rows
    return con


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
        con: Connection = get_connection()
        queryset: Cursor = con.execute(
            "SELECT * FROM articles WHERE id = ?", (id,)
        )

        article: Article = cls(**queryset.fetchone())
        con.close()  # !!! close the connection
        return article

    # classmethod should be preferred over staticmethod
    # if the class is expected to be inherited
    # https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner

    @staticmethod
    def create_table() -> None:
        con: Connection = get_connection()
        with con:  # commit transaction on exit
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS
                articles(id TEXT, author TEXT, title TEXT, content TEXT)
                """
            )
        con.close()

    
    @ensure_table
    def save(self) -> None:
        con: Connection = get_connection()
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
        con: Connection = get_connection()
        with con:
            articles: list[Article] = [
                cls(**row)
                for row in con.execute(
                    """SELECT * FROM articles""",
                )
            ]
        con.close()
        return articles
