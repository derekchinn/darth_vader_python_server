from web import app
from web.routes import WEB_ROOT_PATH
from flask import url_for, request, render_template

@app.route(WEB_ROOT_PATH)
def hello_world():
    return "Hello World!!!!"
