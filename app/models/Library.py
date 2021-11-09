from sqlalchemy.orm import relationship, backref
from ..database import db
from .Book import Book
from .User import User

class Library(db.Model):
    __tablename__ = 'library'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    user = relationship(User, backref=backref("library", cascade="all, delete-orphan"))
    book = relationship(Book, backref=backref("library", cascade="all, delete-orphan"))