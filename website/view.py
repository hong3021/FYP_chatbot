from flask import Blueprint, render_template, request, jsonify
from website.chatbot import response_message
from .model import User

import website.Osintgram as osint
import json

views = Blueprint('views', __name__)

file = True
json = True
output = 'output'
cookies = True
command = False


@views.route('/')
def home():
    return render_template('home.html')


@views.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    message = {"answer": response_message(text)}
    return jsonify(message)


@views.post('/search')
def search_data():
    username = request.get_json().get("username")
    api = osint.Osintgram(username, file, json, command, output, cookies)
    info = api.get_user_info()
    return jsonify(info)




