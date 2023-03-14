from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/readfile/')
def readfile():
    queries = request.args
    file = queries.get('file')
    content = open(file, 'r').read()
    return content