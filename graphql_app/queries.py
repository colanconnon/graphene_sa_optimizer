import graphene
from .sqlalchemy_types import AuthorSQLType, BookSQLType
from .models import Author, Book
from sqlalchemy.orm import joinedload, subqueryload
from flask_jwt_extended import get_jwt_identity
from graphql.utils.ast_to_dict import ast_to_dict
from flask import request
from sqlalchemy.orm import joinedload


class Query(graphene.ObjectType):

    authors = graphene.List(AuthorSQLType)

    books = graphene.List(BookSQLType)

    def resolve_authors(self, info):
        return Author.query.options(*get_optimized_options(Author, info))

    def resolve_books(self, info):
        return Book.query.options(*get_optimized_options(Book, info))
