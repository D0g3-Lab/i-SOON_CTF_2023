#coding=gbk
import json
from flask import Flask, request,  jsonify,send_file,render_template_string
import jwt
import requests
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.config['TEMPLATES_RELOAD']=True

app.config['SECRET_KEY'] = 'fake_flag'
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
response0 = {
    'code': 0,
    'message': 'failed',
    'result': None
}
response1={
    'code': 1,
    'message': 'success',
    'result': current_time
}

response2 = {
    'code': 2,
    'message': 'Invalid request parameters',
    'result': None
}


def auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return 'Invalid token', 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if payload['username'] == User.username and payload['password'] == User.password:
                return func(*args, **kwargs)
            else:
                return 'Invalid token', 401
        except:
            return 'Something error?', 500

    return decorated

@app.route('/',methods=['GET'])
def index():
    return send_file('api-docs.json', mimetype='application/json;charset=utf-8')

@app.route('/api-base/v0/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        User.setUser(username,password)
        token = jwt.encode({'username': username, 'password': password}, app.config['SECRET_KEY'], algorithm='HS256')
        User.setToken(token)
        return jsonify(response1)

    return jsonify(response2),400


@app.route('/api-base/v0/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        try:
            token = User.token
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if payload['username'] == username and payload['password'] == password:
                response = jsonify(response1)
                response.set_cookie('token', token)
                return response
            else:
                return jsonify(response0), 401
        except jwt.ExpiredSignatureError:
            return 'Invalid token', 401
        except jwt.InvalidTokenError:
            return 'Invalid token', 401

    return jsonify(response2), 400

@app.route('/api-base/v0/update', methods=['POST', 'GET'])
@auth
def update_password():
    try:
        if request.method == 'POST':
            try:
                new_password = request.get_json()
                if new_password:

                    update(new_password, User)

                    updated_token = jwt.encode({'username': User.username, 'password': User.password},
                                               app.config['SECRET_KEY'], algorithm='HS256')
                    User.token = updated_token
                    response = jsonify(response1)
                    response.set_cookie('token',updated_token)
                    return response
                else:
                    return jsonify(response0), 401
            except:
                return "Something error?",505
        else:
            return jsonify(response2), 400

    except jwt.ExpiredSignatureError:
        return 'Invalid token', 401
    except jwt.InvalidTokenError:
        return 'Invalid token', 401

def update(src, dst):
    if hasattr(dst, '__getitem__'):
        for key in src:
            if isinstance(src[key], dict):
                 if key in dst and isinstance(src[key], dict):
                    update(src[key], dst[key])
                 else:
                     dst[key] = src[key]
            else:
                dst[key] = src[key]
    else:
        for key, value in src.items() :
            if hasattr(dst,key) and isinstance(value, dict):
                update(value,getattr(dst, key))
            else:
                setattr(dst, key, value)


@app.route('/api-base/v0/logout')
def logout():
    response = jsonify({'message': 'Logout successful!'})
    response.delete_cookie('token')
    return response


@app.route('/api-base/v0/search', methods=['POST','GET'])
@auth
def api():
    if request.args.get('file'):
        try:
            if request.args.get('id'):
                id = request.args.get('id')
            else:
                id = ''
            data = requests.get("http://127.0.0.1:8899/v2/users?file=" + request.args.get('file') + '&id=' + id)
            if data.status_code != 200:
                return data.status_code

            if request.args.get('type') == "text":

                return render_template_string(data.text)
            else:
                return jsonify(json.loads(data.text))
        except jwt.ExpiredSignatureError:
            return 'Invalid token', 401
        except jwt.InvalidTokenError:
            return 'Invalid token', 401
        except Exception:
            return 'something error?'
    else:
        return jsonify(response2)

class MemUser:
    def setUser(self, username, password):
        self.username = username
        self.password = password

    def setToken(self, token):
        self.token = token

    def __init__(self):
        self.username="admin"
        self.password="password"
        self.token=jwt.encode({'username': self.username, 'password': self.password}, app.config['SECRET_KEY'], algorithm='HS256')

if __name__ == '__main__':
    User = MemUser()
    app.run(host='0.0.0.0')
