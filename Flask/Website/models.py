import firebase_admin
from firebase_admin import credentials, db, initialize_app
import base64
from flask_login import UserMixin
    
class User(UserMixin):
    def __init__(self, id, email, password, first_name, profile_picture=None, profile_mimetype=None, is_recognized=False):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.profile_picture = profile_picture
        self.profile_mimetype = profile_mimetype
        self.is_recognized = is_recognized

    @staticmethod
    def get_all():
        """Retrieve all users from Firebase"""
        ref = db.reference('/users')
        all_users = ref.get()
        if all_users:
            return [User(id=uid, **user_info) for uid, user_info in all_users.items()]
        return []

    def get_id(self):
        """Required by Flask-Login"""
        return self.id

    @staticmethod
    def get(user_id):
        """Retrieve a user by id from Firebase"""
        ref = db.reference(f'/users/{user_id}')
        result = ref.get()
        if result:
            return User(id=user_id, **result)
        return None

    def save(self):
        # If the profile picture is already a base64 string, prepare it with the header only if needed
        if self.profile_picture and isinstance(self.profile_picture, str):
            # Check if the header is already present in the string
            if self.profile_picture.startswith("data:"):
                # The header is already present, no need to add it
                encoded_picture = self.profile_picture
            else:
                # The header is not present, add it
                mime = self.profile_mimetype.split('/')[1] if self.profile_mimetype else 'jpeg' # default to 'jpeg' if mimetype not present
                header = f"data:image/{mime};base64,"
                encoded_picture = header + self.profile_picture
        else:
            # If there is no profile picture or it's not a string, set it to None
            encoded_picture = None

        # The rest of your data dictionary looks fine
        data = {
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "profile_mimetype": self.profile_mimetype,
            "is_recognized": self.is_recognized,
            "profile_picture": encoded_picture
        }

        # Update or create the user record in Firebase as you have it
        ref = db.reference(f'/users/{self.id}' if self.id else '/users')
        if self.id:
            ref.update(data)
        else:
            new_ref = ref.push(data)
            self.id = new_ref.key
        return self
    
    @staticmethod
    def find_by_email(email):
        """Find a user by email using Firebase"""
        ref = db.reference('/users')
        all_users = ref.get()
        if all_users:
            for user_id, user in all_users.items():
                if user['email'] == email:
                    return User(id=user_id, **user)
        return None


