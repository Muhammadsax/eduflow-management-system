from flask import Flask
from config import Config
from .extensions import db, login_manager, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # تهيئة الامتدادات
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # إضافة migrate هنا
    
    # سنقوم بتسجيل الـ Blueprints لاحقًا
    
    # إنشاء جداول قاعدة البيانات
    with app.app_context():
        db.create_all()
    
    return app