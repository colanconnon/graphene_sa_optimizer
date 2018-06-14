import graphene
from .sqlalchemy_types import AuthorSQLType, BookSQLType
from .models import Author, Book
from sqlalchemy.orm import joinedload, subqueryload
from flask_jwt_extended import get_jwt_identity
from graphql.utils.ast_to_dict import ast_to_dict
from flask import request
from sqlalchemy.orm import joinedload
from graphene_sa_optimizer import get_optimized_options


class Query(graphene.ObjectType):

    authors = graphene.List(AuthorSQLType)
    author = graphene.Field(AuthorSQLType, id=graphene.Int())

    books = graphene.List(BookSQLType)

    def resolve_author(self, info, id):
        return Author.query.options(*get_optimized_options(Author, info)).get(id)

    def resolve_authors(self, info):
        return Author.query.options(*get_optimized_options(Author, info))

    def resolve_books(self, info):
        return Book.query.options(*get_optimized_options(Book, info))
