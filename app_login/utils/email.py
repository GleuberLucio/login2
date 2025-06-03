from flask_mail import Message, Mail

mail = Mail()


def send_email(subject, recipient, body):
    msg = Message(subject=subject, recipients=[recipient])
    msg.body = body
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_password_reset_email(email, reset_url):
    subject = "Password Reset Request"
    body = f"To reset your password, click the following link: {reset_url}"
    return send_email(subject, email, body)

def send_verification_email(email, verification_link):
    subject = "Email Verification"
    body = f"Please verify your email by clicking the following link: {verification_link}"
    return send_email(subject, email, body)

def send_welcome_email(email):
    subject = "Welcome to Our Service"
    body = "Thank you for signing up! We're glad to have you with us."
    return send_email(subject, email, body)



