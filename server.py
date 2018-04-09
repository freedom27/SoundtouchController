from flask import Flask, request
from libsoundtouch import soundtouch_device
from auth import requires_auth

soundtouch = soundtouch_device('192.168.1.28')
app = Flask(__name__)

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
    return '{"result": "success"}'
    
@app.route('/mute', methods=['POST'])
@requires_auth
def set_mute():
    req_data = request.get_json()
    mute = req_data['mute']
    volume = soundtouch.volume()
    if bool(volume.muted) != bool(mute):
        soundtouch.mute()

    return '{"result": "success"}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')