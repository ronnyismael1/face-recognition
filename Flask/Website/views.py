from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user
from .models import User
from flask_cors import CORS
#from utilities.lock_module import unlock_door

views = Blueprint('views', __name__)
CORS(views)

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

@views.route('/face-detected', methods=['POST'])
def face_detected():
    data = request.json
    user_name = data.get('name', 'Unknown')
    if user_name != 'Unknown':
        flash(f'{user_name} detected! Door unlocking.', 'success')
        #unlock_door(user_name)  # You can uncomment this if unlocking is required
    else:
        flash('Face detected but not recognized.', 'warning')
    return jsonify({'status': 'success', 'message': 'Notification processed.'}), 200