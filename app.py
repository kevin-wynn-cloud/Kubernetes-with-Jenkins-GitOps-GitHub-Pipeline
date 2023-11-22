from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Let's test out that webhook woot!!!'
