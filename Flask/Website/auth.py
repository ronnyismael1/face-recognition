from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import base64


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.find_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                user.logged_in = True  # Set logged_in to True here
                user.save()
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    current_user.logged_in = False  # Set logged_in to False here
    current_user.save()
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        profile_picture = request.files['profilePicture']


        if profile_picture:
            picture_data = profile_picture.read()
            picture_mimetype = profile_picture.mimetype
            # Encode the picture data to base64
            encoded_picture_data = base64.b64encode(picture_data).decode('utf-8')
            header = f"data:{picture_mimetype};base64,"
            encoded_picture = header + encoded_picture_data
        else:
            encoded_picture = None
            picture_mimetype = None

        user = User.find_by_email(email)
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(None, email, generate_password_hash(password1, method='pbkdf2:sha256'), first_name, encoded_picture, picture_mimetype)
            new_user.save()  # This creates a new user in Firebase
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


