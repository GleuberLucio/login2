from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        from . import models
        db.create_all()
    
    from .routes import bp
    from .auth_routes import auth_bp
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    
        
    return app
