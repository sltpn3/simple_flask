from flask import Flask, session, render_template, redirect, make_response, request
from libs.google_auth import _decode_google_user_token
from settings import CLIENT_ID
import uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex


@app.route("/")
def index():
    if 'name' in session:
        r = make_response(render_template('hello.html', session=session))
    else:
        r = make_response(render_template('hello.html'))
    return r


@app.route("/login")
def login():
    session['name'] = 'Aditya'
    return redirect('/')


@app.route("/logout")
def logout():
    session.pop('name')
    return redirect('/')


@app.route("/authorize", methods=['POST'])
def authorize():
    auth_code = request.form.get('credential', None)
    payload = _decode_google_user_token(
        auth_code, CLIENT_ID)
    # print(payload)
    session['name'] = payload['name']
    return redirect('/')
