from ..models.Library import Library
from .BaseRepository import BaseRepository
from ..database import db

class LibraryRepository(BaseRepository):
    def getLibrary(self, userId):
        # return User.query.get(userId).library
        # books = [library.book for library in db.session.query(Library).filter_by(user_id=userId).all()]
        return [library.book for library in db.session.query(Library).filter_by(user_id=userId).all()]

    def addBookToLibrary(self, request, userId):
        try:
            response = request.get_json()
            library = Library(user_id = userId, book_id=response.get('book_id', None))
            # book = Book.query.get(response.get('book_id', None))
            # user = User.query.get(userId)
            # user.library.append(book)
            db.session.add(library)
            db.session.commit()
            return library.book
        except Exception as error:
            db.session.rollback()

    def deleteBookFromLibrary(self, bookId, userId):
        try:
            # book = Book.query.get(bookId)
            # user = User.query.get(userId)
            # user.library.remove(book)
            library = db.session.query(Library).filter_by(user_id=userId, book_id=bookId).first()
            book = library.book
            db.session.delete(library)
            db.session.commit()
            return book
        except Exception as error:
            db.session.rollback()

    # def search(self, request):
    #     response = request.get_json()
    #     searchTerm = response.get('searchTerm', None)
    #     return db.session.query(Book).filter(Book.title.ilike(f'%{searchTerm}%')).all()