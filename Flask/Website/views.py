from flask import Blueprint, render_template, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from .models import User  # Ensure this import is correct based on your project structure
from utilities.lock_module import unlock_door
import base64

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    # Use the current_user from Flask-Login which should be an instance of User or related to it
    return render_template("home.html", user=current_user)

@views.route('/user/<id>/profile-picture')
def profile_picture(id):
    user = User.get(id)
    if not user or not user.profile_picture:
        return 'No profile picture found', 404
    try:
        # Assuming user.profile_picture is the base64 string of the image
        # Check if the profile_picture contains a base64 header
        if ',' in user.profile_picture:
            base64_data = user.profile_picture.split(',')[1]
        else:
            base64_data = user.profile_picture
        
        image_data = base64.b64decode(base64_data)
        return Response(image_data, mimetype=user.profile_mimetype)
    except IndexError as e:
        # Log error e or print to console
        print("Error splitting base64 string:", e)
        return 'Error processing the image data', 500
    except TypeError as e:
        # Log error e or print to console
        print("Error decoding base64 string:", e)
        return 'Error processing the image data', 500


@views.route('/unlock', methods=['POST'])
@login_required
def unlock():
    unlock_door("Manual Override")  # Assume unlock_door is a function defined in utilities.lock_module
    flash('Unlock requested', 'info')
    return redirect(url_for('views.home'))


