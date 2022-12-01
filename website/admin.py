from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from website.chatbot import response_message
from . import db
from .model import User
from flask_login import login_required, current_user, logout_user
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def home():
    if current_user.role != 'admin':
        flash('Only ADMIN can access', category='error')
        return redirect(url_for('views.home'))

    user_amount = str(db.session.query(User).count())
    file_exists = os.path.exists('website/src/intents.json')
    return render_template('AdminDashboard.html', user_amount=user_amount, file_exists=file_exists)


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
    return render_template('AdminManageUser.html', users=users)


@admin.route('/admin/chatbot')
# @login_required
def chatbot():
    if current_user.role != 'admin':
        flash('Only ADMIN can access', category='error')
        return redirect(url_for('views.home'))

    return render_template('testChatbot.html')


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



