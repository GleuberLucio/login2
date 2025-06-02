
class Config:
    """Base configuration class."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'1fa62e99a79097d1a3d1f6f0926076056ca898d3cdb820530246c2a2a893a7d0'
    PASSWORD_RESET_SALT = 'password-reset'
    
    # Configurações do Flask-Mail para envio de emails
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '85e618e597d640'
    MAIL_PASSWORD = '84264ae75c2fcf'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'noreply@seudominio.com'  # pode ser fictício no Mailtrap

