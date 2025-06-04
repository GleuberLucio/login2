from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from flask_login import LoginManager
from .utils.email import mail
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    with app.app_context():
        from .user import user_models
        db.create_all()
    
    from .routes.main_routes import bp
    from .auth.auth_routes import auth_bp
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    
        
    return app
