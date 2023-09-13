from . import db # Import database
from sqlalchemy import Table, Column, Integer, String, MetaData # for raw sql queries
from flask_login import UserMixin # Import UserMixin for user authentication


class User(db.Model, UserMixin): # Create User class
    id = db.Column(db.Integer, primary_key=True) # Create id column
    username = db.Column(db.String(20), nullable=False) # Create username column
    first_name = db.Column(db.String(20), nullable=False) # Create first_name column
    last_name = db.Column(db.String(20), nullable=False) # Create last_name column
    email = db.Column(db.String(40), unique=True, nullable=False) # Create email column
    password = db.Column(db.String(20), nullable=False) # Create password column
    otp_secret = db.Column(db.String(16)) # Create otp_secret column


