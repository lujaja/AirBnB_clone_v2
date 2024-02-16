#!/usr/bin/python3
"""
Starts a simple web app application
"""
from flask import Flask
import html

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    return "c {}".format(html.escape(text).replace('_', ' '))


@app.route("/python",defaults={"text": 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    return "python {}".format(html.escape(text).replace('_', ' '))


if __name__ == "__main__":
    app.run(host='0.0.0.00', port=5000)
