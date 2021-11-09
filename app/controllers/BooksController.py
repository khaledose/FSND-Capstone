from ..repositories.BooksRepository import BooksRepository
from ..auth.auth import requires_auth
from ..exceptions.AuthError import AuthError
from flask import request, jsonify, abort
from flask import Blueprint

book_api = Blueprint('book_api', __name__)
repository = BooksRepository()

@book_api.route('')
def getBooks():
    try:
        books = repository.getAll()
        return jsonify({
            'success': True,
            'books': [book.to_dict() for book in books]
        })
    except Exception as error:
        abort(500)

@book_api.route('/<book_id>')
def getBook(book_id):
    try:
        book = repository.get(book_id)
        
        return jsonify({
            'success': True,
            'book': book.to_dict()
        })
    except Exception as error:
        if book is None:
            abort(404)
        abort(500)

@book_api.route('', methods=['POST'])
@requires_auth(permission='post:books')
def postBook():
    try:
        book = repository.post(request)
        return jsonify({
            'success': True,
            'book': book.to_dict()
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)
    finally:
        repository.close()

@book_api.route('/<book_id>', methods=['PATCH'])
@requires_auth(permission='update:books')
def updateBook(book_id):
    try:
        book = repository.update(book_id, request)
        
        return jsonify({
            'success': True,
            'book': book.to_dict()
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        if book is None:
            abort(404)
        abort(500)
    finally:
        repository.close()

@book_api.route('/<book_id>', methods=['DELETE'])
@requires_auth(permission='delete:books')
def deleteBook(book_id):
    try:
        book = repository.delete(book_id)
        
        return jsonify({
            'success': True,
            'book': book.to_dict()
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        if book is None:
            abort(404)
        abort(500)
    finally:
        repository.close()

@book_api.route('/search', methods=['POST'])
def searchBook():
    try:
        books = repository.search(request)
        return jsonify({
            'success': True,
            'books': [book.to_dict() for book in books]
        })
    except Exception as error:
        abort(500)
    finally:
        repository.close()
