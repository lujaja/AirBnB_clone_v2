#!/usr/bin/python3
"""
    Starts a simple flask web application
"""
from flask import Flask
import html

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def cool(text):
    return "C {}".format(html.escape(text).replace('_', ' '))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
