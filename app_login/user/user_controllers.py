from .user_models import User
from app_login import db
from passlib.hash import pbkdf2_sha256 as hasher

def get_all_users():
    return User.get_all_users()

def get_user_by_id(user_id) -> User:
    """Retrieve a user by their ID."""
    user_id = int(user_id)  # Ensure user_id is an integer
    if user_id <= 0:
        raise ValueError("User ID must be valid.")
    return User.get_by_id(user_id)

def get_user_by_email(email) -> User:
    """Retrieve a user by their email."""
    email = email.lower().strip()
    return User.get_by_email(email)

def format_name(name):
    """Formata o nome completo: primeira letra maiúscula, conectores minúsculos."""
    connectors = {'da', 'de', 'do', 'das', 'dos', 'e'}
    parts = name.strip().split()
    formatted = [
        part.lower() if part.lower() in connectors else part.capitalize()
        for part in parts
    ]
    return ' '.join(formatted)

def create_user(name, email, password):
    name = format_name(name)
    email = email.lower().strip()
    if email == 'gleuberlucio@gmail.com':
        user = User(name=name, email=email, password=password, is_admin=True)
    else:
        user = User(name=name, email=email, password=password)
    return user

def save_user(user):
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user):
    user.name = format_name(user.name)
    db.session.commit()
    return user

def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user

def hash_password(password):
    """Hash a password using PBKDF2."""
    return hasher.hash(password)

def verify_password(stored_password, provided_password):
    """Verify a stored password against a provided password."""
    return hasher.verify(provided_password, stored_password)