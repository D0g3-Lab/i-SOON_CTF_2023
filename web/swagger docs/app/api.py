#coding=gbk
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v2/users', methods=['GET'])
def get_user_info():
    file_path = request.args.get('file')
    id = request.args.get('id')
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                if id:
                    data = json.loads(file_content)
                    for user in data['users']:
                        if user['id'] == int(id):
                            if user:
                                return user
                    else:
                        return 'not found', 404
            return file_content
        except FileNotFoundError:
            return 'error',500

if __name__ == '__main__':
    app.run(port=8899)