from flask import Flask

from github import client

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
