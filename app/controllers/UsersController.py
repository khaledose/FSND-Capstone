from ..repositories.UsersRepository import UsersRepository
from ..auth.auth import requires_auth, verify_decode_jwt, get_token_auth_header
from ..exceptions.AuthError import AuthError
from flask import Blueprint, request, jsonify, abort, redirect, current_app
from authlib.integrations.flask_client import OAuth
from os import environ as env
from six.moves.urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

user_api = Blueprint('user_api', __name__)
oauth = OAuth(current_app)
auth0 = oauth.register(
    'auth0',
    client_id = env.get('AUTH0_CLIENT_ID'),
    client_secret = env.get('AUTH0_CLIENT_SECRET'),
    api_base_url=  env.get('AUTH0_DOMAIN'),
    access_token_url = env.get('AUTH0_DOMAIN') + '/oauth/token',
    authorize_url = env.get('AUTH0_DOMAIN') + '/authorize',
    client_kwargs = {
        'scope': 'openid profile email',
    },
)
repository = UsersRepository()

@user_api.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=env.get('AUTH0_CALLBACK_URL'), audience=env.get('AUTH0_AUDIENCE'))

@user_api.route('/profile')
def profile():
    try:
        token = auth0.authorize_access_token()
        payload = verify_decode_jwt(token['access_token'])
        userinfo = auth0.get('userinfo').json()
        user = repository.get(userinfo['sub'])

        if user is None:
            user = repository.register(userinfo)

        return jsonify({
            'success': True,
            'profile': user.to_dict(),
            'permissions': payload['permissions'],
            'access_token': token['access_token']
            })
    except Exception as error:
        abort(403)

@user_api.route('/logout')
def logout():
    params = {'returnTo': env.get('AUTH0_LOGOUT_REDIRECT'), 'client_id': env.get('AUTH0_CLIENT_ID')}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@user_api.route('')
@requires_auth(permission='view:users')
def getUsers():
    try:
        users = repository.getAll()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users]
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)

@user_api.route('/my_details')
@requires_auth()
def getUser():
    try:     
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
        user = repository.get(payload['sub'])
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)

@user_api.route('', methods=['PATCH'])
@requires_auth()
def updateUser():
    try:
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
        user = repository.update(request.get_json(), payload['sub'])
        
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

@user_api.route('', methods=['DELETE'])
@requires_auth()
def deleteUser():
    try:
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
        repository.delete(payload['sub'])
        logout()
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)
    finally:
        repository.close()
