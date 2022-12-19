from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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


@auth.route('/auth/reset_password',  methods=['GET', 'POST'])
def reset_password():
    # click button
    if request.method == 'POST':
        # get email
        receiver_email = request.form.get('email')
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"

        sender_email = ""
        password = ""
        user_id = User.query.filter_by(email=receiver_email).first()
        if user_id is None:
            flash("Email not exits", category='error')
            return render_template('forgotPassword.html', done=False, user=current_user)
        en_user_id = generate_password_hash(str(user_id.id), method='sha256')

        try:

            # TODO: Send email here

            message = MIMEMultipart("alternative")
            message["Subject"] = "Reset password"
            message["From"] = sender_email
            message["To"] = receiver_email
            link = 'http://127.0.0.1:5000/auth/request?userid=' + en_user_id
            print(en_user_id)
            # sent email with encrpted userid
            html = "<html><body><p>"
            html += 'Hi,This is your reset password link : </br></br> <a href="' + link + '">' + link + '</a>'
            html += "</p></body></html>"

            part2 = MIMEText(html, "html")

            # message.attach(part1)
            message.attach(part2)

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                flash('Email sent', category='success')

        except Exception as e:
            # Print any error messages to stdout
            flash(e, category='error')

        # show massage sent
        return render_template('forgotPassword.html', done=True, user=current_user)

    return render_template('forgotPassword.html', done=False, user=current_user)


@auth.route('/auth/request',  methods=['GET', 'POST'])
def request_reset():
    # get encrpted user id
    args = request.args
    en_user_id = args.get("userid")

    if request.method == 'POST':
        j = 0
        users = User.query.all()
        for i in range(len(users)):
            if check_password_hash(en_user_id, str(users[i].id)):
                j = i
                break

        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_id = j + 1
        if password1 != password2:
            flash('password are not same', category='error')
        elif len(password2) < 8:
            flash("invalid password", category='error')
        else:
            user = User.query.filter_by(id=user_id).first()
            print(user.first_name)
            user.password = generate_password_hash(password1, method='sha256')
            db.session.commit()
            flash('Password updated', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home', user=user))

    return render_template('resetpassword.html', user=None)


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
            new_user = User(email=email, first_name=firstName, role='user', password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)

