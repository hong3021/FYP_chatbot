from flask import Blueprint, render_template, request, jsonify
from website.chatbot import response_message
from flask_login import login_required, current_user
import re

import website.Osintgram as osint
import json

views = Blueprint('views', __name__)

file = True
json = True
output = 'output'
cookies = True
command = False


@views.route('/')
# @login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/osint')
@login_required
def osint_search():
    return render_template('osint.html', user=current_user)


@views.route('/chatBox')
@login_required
def chatBox():
    return render_template('chatInterface.html', user=current_user)


@views.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid

    if re.search("search", text):
        username = str(text).split()[1]
        api = osint.Osintgram(username, file, json, command, output, cookies)
        info = api.get_user_info()
        message = {"answer": info}
        return jsonify(message)
    else:
        message = {"answer": response_message(text)}

    return jsonify(message)


@views.post('/search')
def search_data():
    username = request.get_json().get("username")

    api = osint.Osintgram(username, file, json, command, output, cookies)
    api.get_user_propic()
    info = api.get_user_info()

    return jsonify(info)





