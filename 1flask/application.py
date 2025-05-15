from flask import Flask, request, jsonify, abort, render_template, send_from_directory
import socket
import json
import os

from utils.Button_handler import button_blueprint

host = "127.0.0.1"
port = 5050

app = Flask(__name__)

# 버튼 핸들러 블루프린트 등록
app.register_blueprint(button_blueprint, url_prefix='/buttons')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()
    try:
        if bot_type == 'NORMAL':
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)
        elif bot_type == 'QUICK':
            with open('static/json/quick_reply.json', "r", encoding='utf-8') as json_file:
                jdata = json.load(json_file)
                return jsonify(jdata)
        else:
            abort(404)
    except Exception as ex:
        abort(500)

def get_answer_from_engine(bottype, query):
    mySocket = socket.socket()
    mySocket.connect((host, port))

    json_data = {
        'Query' : query,
        'BotType' : bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    data = mySocket.recv(2048).decode()

    # JSON 변환 전에 NaN을 null로 변환
    if 'NaN' in data:
        data = data.replace('NaN', 'null')

    ret_data = json.loads(data)

    mySocket.close()

    return ret_data

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)