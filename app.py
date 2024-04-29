from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world!"

if __name__ == '__main__':
    app.run(debug=True)