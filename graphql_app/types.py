import graphene
from .models import Book, Author


class AuthorType(graphene.ObjectType):
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    books = graphene.List('graphql_app.types.BookType')

    def resolve_books(self, args, context, info):
        return self.books


class BookType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    isbn = graphene.String()
    author = graphene.Field('graphql_app.types.AuthorType')
    readers = graphene.List('graphql_app.types.ReaderType')

    def resolve_author(self, args, context, info):
        return Author.get_by_id(self.author_id)

    def resolve_readers(self, args, context, info):
        return self.readers


class ReaderType(graphene.ObjectType):
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    books = graphene.List('graphql_app.types.BookType')

    def resolve_books(self, args, context, info):
        return self.books


class ReaderInputType(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
