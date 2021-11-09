from flask import Flask
from flask_cors import CORS
from .database import setup_db
from .controllers.UsersController import user_api
from .controllers.BooksController import book_api
from .controllers.LibraryController import library_api
from flask import jsonify
from .exceptions.AuthError import AuthError

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    CORS(app)
    app.register_blueprint(user_api, url_prefix='/users')
    app.register_blueprint(book_api, url_prefix='/books')
    app.register_blueprint(library_api, url_prefix='/library')
    setup_db(app)
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": error.description
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": error.description
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.description
        }), 401

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": error.description
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()