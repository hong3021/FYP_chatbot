from flask import Blueprint, render_template, request, jsonify
from website.chatbot import response_message
chatBox = Blueprint('chatBox', __name__)


@chatBox.route("/chatBox")
def chat_interface():
    return render_template('chatInterface.html')


@chatBox.post("/chatBox/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    message = {"answer": response_message(text)}
    return jsonify(message)