from ..repositories.LibraryRepository import LibraryRepository
from ..auth.auth import requires_auth, verify_decode_jwt, get_token_auth_header
from ..exceptions.AuthError import AuthError
from flask import request, jsonify, abort
from flask import Blueprint

library_api = Blueprint('library_api', __name__)
repository = LibraryRepository()

@library_api.route('')
@requires_auth()
def getUserLibrary():
    try:
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
        books = repository.getLibrary(payload['sub'])
        return jsonify({
            'success': True,
            'books': [book.to_dict() for book in books]
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)

@library_api.route('', methods=['POST'])
@requires_auth()
def addBookToLibrary():
    try:
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
        book = repository.addBookToLibrary(request.get_json(), payload['sub'])
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

@library_api.route('/<book_id>', methods=['DELETE'])
@requires_auth()
def deleteBookFromLibrary(book_id):
    try:
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
        book = repository.deleteBookFromLibrary(book_id, payload['sub'])
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