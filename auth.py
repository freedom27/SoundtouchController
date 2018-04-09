from functools import wraps
from flask import request, Response
from config import config

def check_credentials(credentials):
    """This function is called to check if a username /
    password combination is valid.
    """
    return (credentials.username == config['credentials']['username'] and 
            credentials.password == config['credentials']['password'])

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Please login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_credentials(auth):
            return authenticate()
        return f(*args, **kwargs)
    return decorated