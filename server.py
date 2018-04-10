from flask import Flask, request
from libsoundtouch import soundtouch_device
from auth import requires_auth
from config import config

soundtouch = soundtouch_device(config['soundtouch']['ip'])
app = Flask(__name__)

BASE_SOUNDTOUCH_URL = '/soundtouch'
SUCCESS_RESPONSE_JSON = '{"result": "success"}'

@app.route(BASE_SOUNDTOUCH_URL)
def index():
    return 'Welcome to the Soundtouch Control System'
    
@app.route(BASE_SOUNDTOUCH_URL+'/volume', methods=['POST'])
@requires_auth
def set_volume():
    req_data = request.get_json()
    volume = req_data['volume']
    soundtouch.set_volume(volume)
    return SUCCESS_RESPONSE_JSON
    
@app.route(BASE_SOUNDTOUCH_URL+'/source', methods=['POST'])
@requires_auth
def set_source():
    req_data = request.get_json()
    source = req_data['source']
    if source == 'tv':
        soundtouch.select_source_tv()
    elif source == 'bluetooth':
        soundtouch.select_source_bluetooth()
    return SUCCESS_RESPONSE_JSON
    
@app.route(BASE_SOUNDTOUCH_URL+'/mute', methods=['POST'])
@requires_auth
def set_mute():
    req_data = request.get_json()
    mute = req_data['mute']
    volume = soundtouch.volume()
    if bool(volume.muted) != bool(mute):
        soundtouch.mute()
    return SUCCESS_RESPONSE_JSON

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')