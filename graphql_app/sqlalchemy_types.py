import graphene
from .models import Book, Author, Reader
from graphene_sqlalchemy import SQLAlchemyObjectType


class AuthorSQLType(SQLAlchemyObjectType):
    id = graphene.Int()

    class Meta:
        model = Author


class BookSQLType(SQLAlchemyObjectType):
    id = graphene.Int()

    class Meta:
        model = Book


class ReaderSQLType(SQLAlchemyObjectType):
    id = graphene.Int()

    class Meta:
        model = Reader
