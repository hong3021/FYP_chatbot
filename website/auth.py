from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfuly', category='success')
                login_user(user, remember=True )
                if user.role == 'admin':
                    return redirect(url_for('admin.home'))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/auth/Signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4 :
            flash('Email not valid', category='error')
        elif len(firstName) < 2:
            flash('FirstName not valid', category='error')
        elif password1 != password2:
            flash('password are not same', category='error')
        elif len(password2) < 8:
            flash("invalid password", category='error')
        else:
            new_user = User(email=email, first_name=firstName, role='admin', password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)


# @auth.route('/auth/admin', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         admin = Admin.query.filter_by(username=username).first()
#         if admin:
#             if check_password_hash(admin.password, password):
#                 flash('logged in successfuly', category='success')
#                 login_user(admin, remember=True )
#                 return redirect(url_for('admin.home'))
#             else:
#                 flash('Incorrect password', category='error')
#         else:
#             flash('Username does not exist', category='error')
#
#     return render_template("admin/Adminlogin.html", user=current_user)