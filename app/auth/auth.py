import json
from re import A
from flask import request, abort, current_app, session
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from authlib.integrations.flask_client import OAuth
from os import environ as env
from ..exceptions.AuthError import AuthError

ALGORITHMS = ['RS256']

def setup_auth():
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
    return auth0


## Auth Header

'''
    it attempts to get the header from the request
    it raises an AuthError if no header is present
    it attempts to split bearer and the token
    it raises an AuthError if the header is malformed
    returns the token part of the header
'''
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    it raises an AuthError if permissions are not included in the payload
    it raises an AuthError if the requested permission string is not in the payload permissions array
    returns true otherwise
'''
def check_permissions(permission=''):
    print(session['permissions'])
    if 'permissions' not in session:
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'permissions are not included in the payload'
        }, 400)
    if permission != '' and permission not in session['permissions']:
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'permission is not in the permissions array'
        }, 403)
    return True
    

def check_auth():
    if 'profile' not in session:
        raise AuthError({
            'code': 'not_logged_in',
            'description': 'User ust be logged in.".'
        }, 401)
    return True
'''
    @INPUTS
        token: a json web token (string)
    it verifies the token using Auth0 /.well-known/jwks.json
    it decodes the payload from the token
    it validates the claims
    returns the decoded payload
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(env.get('AUTH0_DOMAIN')+'/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=env.get('AUTH0_AUDIENCE'),
                issuer=env.get('AUTH0_DOMAIN') + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
    it uses the get_token_auth_header method to get the token
    it uses the verify_decode_jwt method to decode the jwt
    it uses the check_permissions method validate claims and check the requested permission
    returns the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                check_auth()
                # token = get_token_auth_header()
                # payload = verify_decode_jwt(token)
                check_permissions(permission)
            except Exception as error:
                abort(error.status_code)
            
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator