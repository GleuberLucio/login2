from itsdangerous import URLSafeTimedSerializer
from config.config import Config
from flask import url_for
from ..utils.email import send_password_reset_email
from passlib.hash import pbkdf2_sha256 as hasher

def generate_token(email):
    """Generate a secure token for password reset."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.PASSWORD_RESET_SALT)

def verify_token(token):
    """Verify the token and return the email if valid."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=Config.PASSWORD_RESET_SALT, max_age=3600)  # Token valid for 1 hour
        return email
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
    
def send_password_reset_link(email, token):
    """Send a password reset email to the user."""
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    if send_password_reset_email(email, reset_url):
        return True
    else:
        print("Failed to send password reset email.")
        return False
    
    
def hash_password(password):
    """Hash a password using PBKDF2."""
    return hasher.hash(password)

def verify_password(stored_password, provided_password):
    """Verify a stored password against a provided password."""
    return hasher.verify(provided_password, stored_password)    
    