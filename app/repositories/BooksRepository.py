from ..models.Book import Book
from .BaseRepository import BaseRepository
from ..database import db

class BooksRepository(BaseRepository):
    def getAll(self):
        return Book.query.all()

    def get(self, id):
        return Book.query.get(id)

    def post(self, body):
        try:
            newBook = Book(title=body.get('title', None),
                            description=body.get('description', None),
                            author=body.get('author', None)
                        )
            db.session.add(newBook)
            db.session.commit()
            return newBook
        except Exception as error:
            db.session.rollback()

    def update(self, id, body):
        try:
            book = self.get(id)
            book.title = body.get('title', book.title)
            book.description  = body.get('description', book.description)
            book.author  = body.get('author', book.author)
            db.session.commit()
            return book
        except Exception as error:
            db.session.rollback()

    def search(self, body):
        searchTerm = body.get('searchTerm', '')
        return db.session.query(Book).filter(Book.title.ilike(f'%{searchTerm}%')).all()