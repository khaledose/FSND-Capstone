from ..models.Book import Book
from .BaseRepository import BaseRepository
from ..database import db

class BooksRepository(BaseRepository):
    def getAll(self):
        return Book.query.all()

    def get(self, id):
        return Book.query.get(id)

    def post(self, request):
        try:
            response = request.get_json()
            newBook = Book(title=response.get('title', None),
                            description=response.get('description', None),
                            author=response.get('author', None)
                        )
            db.session.add(newBook)
            db.session.commit()
            return newBook
        except Exception as error:
            db.session.rollback()

    def update(self, id, request):
        try:
            book = self.get(id)
            response = request.get_json()
            book.title = response.get('title', None)
            book.description  = response.get('description', None)
            book.author  = response.get('author', None)
            db.session.commit()
            return book
        except Exception as error:
            db.session.rollback()

    def search(self, request):
        response = request.get_json()
        searchTerm = response.get('searchTerm', None)
        return db.session.query(Book).filter(Book.title.ilike(f'%{searchTerm}%')).all()