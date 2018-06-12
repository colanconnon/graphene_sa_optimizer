import graphene

from .models import Author, Book, Reader
from .types import AuthorType, BookType, ReaderInputType, ReaderType


class AuthorMutation(graphene.Mutation):

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    author = graphene.Field(AuthorType)

    def mutate(self, info, first_name, last_name):
        author = Author.create(
            first_name=first_name,
            last_name=last_name
        )
        return AuthorMutation(author=author)


class BookMutation(graphene.Mutation):

    class Arguments:
        isbn = graphene.String(required=True)
        title = graphene.String(required=True)
        author_id = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, isbn, author_id):
        book = Book.create(
            title=title,
            isbn=isbn,
            author_id=author_id
        )
        return BookMutation(book=book)


class AddReaderToBookMutation(graphene.Mutation):

    class Arguments:
        book_id = graphene.Int()
        reader = graphene.Argument(ReaderInputType)

    reader = graphene.Field(ReaderType)

    def mutate(self, args, context, book_id, reader):
        reader = Reader.create(
            first_name=reader['first_name'],
            last_name=reader['last_name']
        )
        book = Book.get_by_id(book_id)
        reader.books.append(book)
        reader.save()
        return AddReaderToBookMutation(reader=reader)


class Mutation(graphene.ObjectType):
    create_author = AuthorMutation.Field()
    create_book = BookMutation.Field()
    add_reader_to_book = AddReaderToBookMutation.Field()
