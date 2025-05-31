from app import db
from passlib.hash import pbkdf2_sha256 as hasher

class User(db.Model):
    """User model for the application."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def __init__(self, name, email, password):
        """Initialize a new user."""
        self.name = name
        self.email = email
        self.password_hash = hasher.hash(password)
        
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