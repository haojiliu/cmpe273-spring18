from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/users/<int:uid>', methods=['GET'])
def users_get(uid):
    return (jsonify({'id': 1, 'name': 'foo'}), 200)

@app.route('/users', methods=['POST'])
def users_post():
    user_name = request.form['name']
    return (jsonify({'id': 1, 'name': 'foo'}), 201)

@app.route('/users/<int:uid>', methods=['DELETE'])
def users_delete(uid):
    return ('', 204)

# >>> import requests
# >>> r = requests.post('http://127.0.0.1:5000/users', data={"name":"foo"})
# >>> r
# <Response [201]>
# >>> r = requests.delete('http://127.0.0.1:5000/users')
# >>> r
# <Response [405]>
# >>> r = requests.delete('http://127.0.0.1:5000/users/1')
# >>> r
# <Response [204]>
# >>> r = requests.get('http://127.0.0.1:5000/users/1')
# >>> r
# <Response [200]>
# >>> r = requests.get('http://127.0.0.1:5000/')
# >>> r
# <Response [200]>
