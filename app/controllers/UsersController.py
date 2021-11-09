from ..repositories.UsersRepository import UsersRepository
from ..auth.auth import requires_auth, setup_auth, verify_decode_jwt
from ..exceptions.AuthError import AuthError
from flask import Blueprint, request, jsonify, abort, session, redirect
from os import environ as env
from six.moves.urllib.parse import urlencode

user_api = Blueprint('user_api', __name__)
# auth0 = setup_auth()
repository = UsersRepository()

@user_api.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=env.get('AUTH0_CALLBACK_URL'), audience=env.get('AUTH0_AUDIENCE'))

@user_api.route('/profile')
def profile():
    try:
        print(request.args.get('state'), session.get('_auth0_authlib_state_'))
        token = auth0.authorize_access_token()
        payload = verify_decode_jwt(token['access_token'])
        userinfo = auth0.get('userinfo').json()
        user = repository.getByEmail(userinfo['email'])

        if user is None:
            user = repository.register(userinfo)
        session['jwt_payload'] = userinfo
        session['profile'] = user.to_dict()
        session['permissions'] = payload['permissions']

        return jsonify({
            'success':True,
            'profile': session['profile'],
            'permissions': session['permissions']
            })
    except Exception as error:
        abort(403)

@user_api.route('/logout')
def logout():
    session.clear()
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
        return jsonify({
            'success': True,
            'user': session['profile']
        })
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)

@user_api.route('', methods=['PATCH'])
@requires_auth()
def updateUser():
    try:
        user = repository.update(request, session['profile'])
        
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
        repository.delete(session['profile']['id'])
        logout()
    except AuthError as auth_error:
        print(auth_error)
    except Exception as error:
        abort(500)
    finally:
        repository.close()

@user_api.route('/session', methods=['POST'])
def addSession():
    print("a7a1")
    response = request.get_json()
    print("a7a2")
    user = repository.get(response.get('id', None))
    print("a7a3")
    session['profile'] = user.to_dict()
    print("a7a4")
    session['permissions'] = response.get('permissions', None)
    print("a7a5")
    return jsonify({
            'success': True,
            'user': user.to_dict()
        })