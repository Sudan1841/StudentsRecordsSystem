
from app import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from flask_login import login_required, current_user
from flask import redirect, url_for, abort, flash

# Your model definitions


class User(db.Model, UserMixin):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    about = db.Column(db.Text)
    passwd_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.passwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwd_hash, password)




class St(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    grade = db.Column(db.String(10))
    user_id = db.Column(db.String(64), db.ForeignKey("user.id"), primary_key=True)
   
















