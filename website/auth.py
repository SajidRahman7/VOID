from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Email already exists. Please log in.', 'danger')
        elif password1 != password2:
            flash('Passwords do not match.', 'danger')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # 👈 Use Flask-Login here
            flash('Logged in successfully!', 'success')
            return redirect(url_for('views.home'))  # 👈 Home is at `/`
        else:
            flash('Incorrect email or password.', 'danger')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()  # 👈 Use Flask-Login here
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
