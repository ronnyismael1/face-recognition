from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user
from .models import User
#from utilities.lock_module import unlock_door

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/user/<int:id>/profile-picture')
def profile_picture(id):
    user = User.query.get(id)
    if not user or not user.profile_picture:
        return 'No profile picture found', 404  # You can also redirect to a default image here
    return Response(user.profile_picture, mimetype=user.profile_mimetype)

@views.route('/unlock', methods=['POST'])
@login_required
def unlock():
    #unlock_door("Manual Override")  # Call the unlock function from lock_module
    flash('Unlock requested', 'info')  # Inform the user
    return redirect(url_for('views.home'))
