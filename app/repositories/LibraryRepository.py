from ..models.Library import Library
from .BaseRepository import BaseRepository
from ..database import db

class LibraryRepository(BaseRepository):
    def getLibrary(self, userId):
        return [library.book for library in db.session.query(Library).filter_by(user_id=userId).all()]

    def addBookToLibrary(self, body, userId):
        try:
            library = Library(user_id = userId, book_id=body.get('book_id', None))
            db.session.add(library)
            db.session.commit()
            return library.book
        except Exception as error:
            db.session.rollback()

    def deleteBookFromLibrary(self, bookId, userId):
        try:
            library = db.session.query(Library).filter_by(user_id=userId, book_id=bookId).first()
            book = library.book
            db.session.delete(library)
            db.session.commit()
            return book
        except Exception as error:
            db.session.rollback()