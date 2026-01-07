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
    
    # تسجيل Blueprint لوحة التحكم الرئيسية
    from eduflow_app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # سنقوم بتسجيل باقي الـ Blueprints لاحقًا عندما ننشئها
    # from eduflow_app.academic import bp as academic_bp
    # app.register_blueprint(academic_bp, url_prefix='/academic')
    # from eduflow_app.library import bp as library_bp
    # app.register_blueprint(library_bp, url_prefix='/library')
    # from eduflow_app.finance import bp as finance_bp
    # app.register_blueprint(finance_bp, url_prefix='/finance')
    # from eduflow_app.forum import bp as forum_bp
    # app.register_blueprint(forum_bp, url_prefix='/forum')
    # from eduflow_app.communication import bp as communication_bp
    # app.register_blueprint(communication_bp, url_prefix='/communication')
    
    # إنشاء جداول قاعدة البيانات
    with app.app_context():
        db.create_all()
    
    return app