from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from website.chatbot import response_message
from . import db
from .model import User, Admin
from flask_login import login_required, current_user, logout_user
import json
import os


admin = Blueprint('admin', __name__)


@admin.route('/admin')
# @login_required
def home():
    user_amount = str(db.session.query(User).count())
    file_exists = os.path.exists('website/src/intents.json')
    return render_template('AdminDashboard.html', user_amount=user_amount, file_exists=file_exists)


@admin.route('/admin/user', methods=['POST', 'GET'])
# @login_required
def manage_user():
    users = User.query.all()

    for user in users:
        print(user.first_name)

    return render_template('AdminManageUser.html')


@admin.route('/admin/chatbot')
# @login_required
def chatbot():
    return render_template('')

@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))