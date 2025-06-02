from itsdangerous import URLSafeTimedSerializer
from config.config import Config
from flask_mail import Message
from flask import url_for
from app_login import mail
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
    
def send_password_reset_email(email, token):
    """Send a password reset email to the user."""
    msg = Message(subject="Password Reset Request",
                  sender=Config.MAIL_DEFAULT_SENDER,
                  recipients=[email])
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg.body = f"To reset your password, click the following link: {reset_url}"
    
    try:
        mail.send(msg)
        print("Password reset email sent successfully.")
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
    
    return msg
    
    
def hash_password(password):
    """Hash a password using PBKDF2."""
    return hasher.hash(password)

def verify_password(stored_password, provided_password):
    """Verify a stored password against a provided password."""
    return hasher.verify(provided_password, stored_password)    
    