from ..repositories.LibraryRepository import LibraryRepository
from ..auth.auth import requires_auth
from ..exceptions.AuthError import AuthError
from flask import request, jsonify, abort, session
from flask import Blueprint

library_api = Blueprint('library_api', __name__)
repository = LibraryRepository()

@library_api.route('')
@requires_auth()
def getUserLibrary():
    # try:
        library = repository.getLibrary(session['profile']['id'])
        return jsonify({
            'success': True,
            'user': session['profile'],
            'books': [book.to_dict() for book in library]
        })
    # except AuthError as auth_error:
    #     print(auth_error)
    # except Exception as error:
    #     abort(500)

@library_api.route('', methods=['POST'])
@requires_auth()
def addBookToLibrary():
    try:
        book = repository.addBookToLibrary(request, session['profile']['id'])
        return jsonify({
            'success': True,
            'user': session['profile'],
            'book': book.to_dict()
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)
    finally:
        repository.close()

@library_api.route('/<book_id>', methods=['DELETE'])
@requires_auth()
def deleteBookFromLibrary(book_id):
    try:
        book = repository.deleteBookFromLibrary(book_id, session['profile']['id'])
        
        return jsonify({
            'success': True,
            'user': session['profile'],
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