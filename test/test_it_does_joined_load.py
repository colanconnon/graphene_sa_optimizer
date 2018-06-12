import json
import os
import tempfile

import pytest

from graphql_app import create_app, db
from graphql_app.schema import schema
from graphql_app.models import Author, Book, Reader
from .utils import create_resolve_info, get_query
from graphene_sa_optimizer import get_optimized_joins
from sqlalchemy.orm import joinedload, load_only


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # create the app with common test config
    app = create_app()

    # create the database and load test data
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_it_loads_related_fields_for_author(client, app):
    query = """
    {
        authors{
            id
            firstName
            books
            {
                id
                isbn
                readers {
                    id
                }
            }
        }
    }
    """
    with app.app_context():
        author = Author.create(first_name="test1", last_name="test2")
        book = Book.create(title="test", isbn="r123213", author=author)
        reader = Reader.create(first_name="test", last_name="test2")
        reader.books.append(book)
        reader.save()
        info = create_resolve_info(schema, query)
        result_q = Author.query.options(*get_optimized_joins(Author, info))
        expected_q = Author.query.options(
            joinedload("books").load_only("id", "isbn"),
            joinedload("books.readers").load_only("id"),
            load_only("id", "first_name"),
        )
        assert str(expected_q) == str(result_q)


def test_it_loads_related_fields_for_books(client, app):
    query = """
    {
       books {
           id
           isbn
           author {
               id
               lastName
               books {
                   id
                   isbn
               }
           }
           readers {
               id
               lastName
           }
       }
    }
    """
    with app.app_context():
        author = Author.create(first_name="test1", last_name="test2")
        book = Book.create(title="test", isbn="r123213", author=author)
        reader = Reader.create(first_name="test", last_name="test2")
        reader.books.append(book)
        reader.save()
        info = create_resolve_info(schema, query)
        result_q = Book.query.options(*get_optimized_joins(Book, info))
        expected_q = Book.query.options(
            joinedload("author").load_only("id", "last_name"),
            joinedload("author.books").load_only("id", "isbn"),
            joinedload("readers").load_only("id", "last_name"),
            load_only("id", "isbn"),
        )
        assert str(expected_q) == str(result_q)
