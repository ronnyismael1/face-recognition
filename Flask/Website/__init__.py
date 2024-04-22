from flask import Flask
import firebase_admin
from firebase_admin import credentials, db as firebase_db, initialize_app
def initialize_firebase():
    # Path to your Firebase Admin SDK service account key file
    #add cred and firebase initialization here
    cred = credentials.Certificate('Flask/Website/static/yummy.json')
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facelock-b410f-default-rtdb.firebaseio.com/'
    })

def create_app():
    app = Flask(__name__)
    initialize_firebase()
    listen_for_user_updates()
    return app

def listen_for_user_updates():
    ref = firebase_db.reference('/users')
    
    def user_changed(event):
        print('Data changed:', event.data)
    
    ref.listen(user_changed)


    """login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User  # Import here to avoid circular dependency

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)  # Use the Firebase admin SDK to load user

    return app"""
