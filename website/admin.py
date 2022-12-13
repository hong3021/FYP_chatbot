from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, Flask, send_from_directory, send_file
from jinja2 import UndefinedError

from website.chatbot import response_message
from website.training import train
from . import db
from .model import User, Chatlog
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)
UPLOAD_FOLDER = 'website/src'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@admin.route('/admin')
@login_required
def home():
    if current_user.role != 'admin':
        flash('Only ADMIN can access', category='error')
        return redirect(url_for('views.home'))

    user_amount = str(db.session.query(User).count())
    file_exists = os.path.exists('website/src/intents.json')
    return render_template('admin/AdminDashboard.html', user_amount=user_amount, file_exists=file_exists)


@admin.route('/admin/user', methods=['POST', 'GET'])
# @login_required
def manage_user():
    if current_user.role != 'admin':
        flash('Only ADMIN can access', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        

        delete = request.form.get('delete')
        x = db.session.query(User).get(delete)
        db.session.delete(x)
        db.session.commit()
        flash('User Deleted', category='success')
    users = User.query.all()

    return render_template('admin/AdminManageUser.html', users=users)


@admin.route('/admin/chatbot', methods=['POST', 'GET'])
# @login_required
def chatbot():
    if current_user.role != 'admin':
        flash('Only ADMIN can access', category='error')
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        if request.form.get('submit') == 'submit':
            f = request.files['intent_file']
            f.filename = "intents.json"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            flash('Intent uploaded', category='success')
        if request.form.get('train') == 'train':
            train()
            flash('Done', category='success')

    return render_template('admin/testChatbot.html')


@admin.route('admin/chatlog/<int:user_id>', methods=['POST', 'GEt'])
@login_required
def view_chatlog(user_id):
    json_data = {}
    data = []

    chatlogs = Chatlog.query.filter_by(user_id=user_id).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'download':
            for chatlog in chatlogs:
                chat ={
                    'id': str(chatlog.id),
                    'message': chatlog.message,
                    'answer': chatlog.answer,
                    'date': str(chatlog.date)
                }
                data.append(chat)

            json_data['chatlogs'] = data
            filename = str(chatlogs[0].id) + '_chatlog.json'
            json_file_name = "website/output" + "/" + filename
            with open(json_file_name, 'w') as f:
                json.dump(json_data, f)

            return redirect(url_for('admin.download', filename=filename, src='output'))

    return render_template('admin/chatlog.html', chatlogs=chatlogs)


@admin.post("/admin/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    message = {"answer": response_message(text)}
    return jsonify(message)


@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@admin.route('admin/download', methods=['GET', 'POST'])
@login_required
def download():
    args = request.args
    filename = args.get("filename")
    src = args.get("src")
    uploads = os.path.join(src, filename)
    return send_file(uploads, as_attachment=True)



