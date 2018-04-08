from flask import Flask, request, Response
from functools import wraps
from libsoundtouch import soundtouch_device

soundtouch = soundtouch_device('192.168.1.28')
app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'bose_user' and password == 'letmedoit'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return 'Welcome to the Soundtouch Control System'
    
@app.route('/volume', methods=['POST'])
@requires_auth
def set_volume():
    req_data = request.get_json()
    volume = req_data['volume']
    soundtouch.set_volume(volume)
    return '{"result": "success"}'
    
@app.route('/source', methods=['POST'])
@requires_auth
def set_source():
    req_data = request.get_json()
    source = req_data['source']
    if source == 'tv':
        soundtouch.select_source_tv()
    elif source == 'bluetooth':
        soundtouch.select_source_bluetooth()
    return '{result: "success"}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')