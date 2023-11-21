# Import the Flask class from the flask module
from flask import Flask

# Create an instance of the Flask class with the name of the running application as an argument
app = Flask(__name__)

# Define a route for the root URL ('/')
@app.route('/')
def hello_world():
    # Return a message when the root URL is accessed
    return 'Please subscribe, like, and comment on this video, TY!!!'
