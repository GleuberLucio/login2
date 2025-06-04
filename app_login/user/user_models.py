from app_login import db
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """User model for the application."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
        
    def __init__(self, name, email, password, is_admin=False, is_active=True, is_verified=False):
        """Initialize a new user."""
        self.name = name
        self.email = email
        self.password_hash = hasher.hash(password)
        self.is_admin = is_admin
        self.is_active = is_active
        self.is_verified = is_verified
        
        return self

    def __repr__(self):
        return f'<User {self.name}>'
   
    @classmethod
    def get_by_id(cls, user_id):
        """Get a user by their ID."""
        return cls.query.get(user_id)
    @classmethod
    def get_by_email(cls, email):
        """Get a user by their email."""
        return cls.query.filter_by(email=email).first()
    @classmethod
    def get_all_users(cls):
        """Get all users."""
        return cls.query.all()