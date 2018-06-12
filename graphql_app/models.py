# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from .database import Column, Model, SurrogatePK, db, reference_col, relationship
import datetime
import jwt
import os
from werkzeug.security import generate_password_hash, \
     check_password_hash

class Author(SurrogatePK, Model):

    __tablename__ = 'authors'
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    created_at = Column(db.DateTime, nullable=False,
                        default=dt.datetime.utcnow)


book_reader_association_table = db.Table('book_readers', db.metadata,
                                         Column('books_id', db.Integer,
                                                db.ForeignKey('books.id')),
                                         Column('readers_id', db.Integer,
                                                db.ForeignKey('readers.id'))
                                         )


class Book(SurrogatePK, Model):
    __tablename__ = 'books'
    title = Column(db.String(50), nullable=False)
    isbn = Column(db.String(30), nullable=False)
    author_id = reference_col('authors', nullable=False)
    author = relationship('Author', backref='books')
    readers = relationship(
        "Reader",
        secondary=book_reader_association_table,
        back_populates="books")


class Reader(SurrogatePK, Model):
    __tablename__ = 'readers'
    first_name = Column(db.String(50), nullable=False)
    last_name = Column(db.String(50), nullable=False)
    books = relationship(
        "Book",
        secondary=book_reader_association_table,
        back_populates="readers")


class User(SurrogatePK, Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password_hash = db.Column(db.String())
    
    @classmethod
    def get_password_hash(cls, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_valid(self):
        if self.username is None or len(self.username) == 0:
            return False
        return True
