from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

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
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html")


@auth.route('/auth/logout')
def logout():
    return '<h1>loguot</h1>'


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
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html")
