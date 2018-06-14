import json
import os
import tempfile

import pytest

from graphql_app import create_app, db
from graphql_app.schema import schema
from graphql_app.models import Author, Book, Reader
from .utils import create_resolve_info, get_query
from graphene_sa_optimizer import get_optimized_options
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
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()



def test_it_loads_one_author(client, app):
    query = """
    query getAuthor($id: Int!){
        author(id: $id){
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
        result = schema.execute(query, variable_values={'id': author.id}).data
        assert result['author']['firstName'] == author.first_name
        assert result['author']['books'][0]['isbn'] == book.isbn

def test_it_loads_authors(client, app):
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
        result = schema.execute(query, variable_values={'id': author.id})
        assert result.data['authors'][0]['firstName'] == author.first_name
        assert result.data['authors'][0]['books'][0]['isbn'] == book.isbn