from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, ForeignKey
from ..database import db
from .Book import Book
from .User import User

class Library(db.Model):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(64), ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

    user = relationship(User, backref=backref("library", cascade="all, delete-orphan"))
    book = relationship(Book, backref=backref("library", cascade="all, delete-orphan"))