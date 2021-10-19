from Repositories.UsersRepository import UsersRepository
from flask import request, jsonify, abort
from flask import Blueprint

user_api = Blueprint('user_api', __name__)
repository = UsersRepository()

@user_api.route('')
def getUsers():
    try:
        users = repository.getAll()
        print(users)
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users]
        })
    except Exception as error:
        abort(500)

@user_api.route('/<user_id>')
def getUser(user_id):
    try:
        user = repository.get(user_id)
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    except Exception as error:
        if user is None:
            abort(404)
        abort(500)

@user_api.route('', methods=['POST'])
def postUser():
    try:
        user = repository.post(request)
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    except Exception as error:
        abort(500)
    finally:
        repository.close()

@user_api.route('/<user_id>', methods=['PATCH'])
def updateUser(user_id):
    try:
        user = repository.update(user_id, request)
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    except Exception as error:
        if user is None:
            abort(404)
        abort(500)
    finally:
        repository.close()

@user_api.route('/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    try:
        user = repository.delete(user_id)
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    except Exception as error:
        if user is None:
            abort(404)
        abort(500)
    finally:
        repository.close()