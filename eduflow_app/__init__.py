from flask import Flask
from config import Config
from .extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # سنقوم بتسجيل الـ Blueprints لاحقًا
    
    with app.app_context():
        db.create_all()
    
    return app