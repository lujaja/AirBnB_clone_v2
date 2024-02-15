#!/usr/bin/python3
"""
    This is a simple flask web app
"""
from flask import Flask
# When you run this script directly name will be set to main
app = Flask(__name__)


# Tells flask to call hello function when root URL is accessed
@app.route("/", strict_slashes=False)
def hello():
    """Renders Hello world to the user"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
