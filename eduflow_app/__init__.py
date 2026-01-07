from flask import Flask
from config import Config
from .extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # تهيئة الامتدادات
    db.init_app(app)
    login_manager.init_app(app)
    
    # تسجيل Blueprint وحدة المصادقة
    from eduflow_app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # سنقوم بتسجيل باقي الـ Blueprints لاحقًا
    
    # إنشاء جداول قاعدة البيانات
    with app.app_context():
        db.create_all()
    
    return app