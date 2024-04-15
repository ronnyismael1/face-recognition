from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    profile_picture = db.Column(db.LargeBinary)
    profile_mimetype = db.Column(db.String(256))
    is_recognized = db.Column(db.Boolean, default=False)  # New field to track recognition status
    logged_in = db.Column(db.Boolean, default=False)