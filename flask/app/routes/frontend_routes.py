from flask import render_template

from app.main import app


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
