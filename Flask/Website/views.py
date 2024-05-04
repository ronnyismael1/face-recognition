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
        # Assuming user. profile_picture is the base64 string of the image
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



@views.route('/unlock', methods=['POST'])
@login_required  # This decorator requires a user to be logged in to access this route.
def unlock():
    unlock_door("Automatic Recognition")  # Assuming unlock_door is defined elsewhere
    flash('Door unlocked!', 'success')
    return redirect(url_for('views.home'))  


