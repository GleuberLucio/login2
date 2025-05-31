from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

db = SQLAlchemy()
app = Flask(__name__)

def init_app():
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        from . import models
        db.create_all()
    
    from . import routes
    app.register_blueprint(routes.bp)
        
    return app
    