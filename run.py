import sys
import os

# أضف المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from eduflow_app import create_app
    
    app = create_app()
    
    @app.route('/')
    def home():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>EduFlow - Home</title>
            <style>
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: Arial, sans-serif;
                    color: white;
                }
                .container {
                    text-align: center;
                    background: rgba(255,255,255,0.1);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }
                h1 {
                    font-size: 3em;
                    margin-bottom: 20px;
                }
                .status {
                    font-size: 1.2em;
                    padding: 10px 20px;
                    background: rgba(0,255,0,0.2);
                    border-radius: 10px;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎓 EduFlow</h1>
                <div class="status">✅ النظام يعمل بنجاح!</div>
                <p>Flask + SQLAlchemy + Login Manager</p>
            </div>
        </body>
        </html>
        '''
    
    @app.route('/test-db')
    def test_db():
        from eduflow_app.models import User
        from eduflow_app.extensions import db
        
        # محاولة إنشاء المستخدم الأول
        try:
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', email='admin@eduflow.com')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                return '✅ تم إنشاء قاعدة البيانات والمستخدم الأول!'
            else:
                return '✅ قاعدة البيانات موجودة بالفعل!'
        except Exception as e:
            return f'❌ خطأ: {str(e)}'
    
    if __name__ == '__main__':
        print("🚀 تشغيل EduFlow على http://localhost:5000")
        print("📊 صفحة اختبار قاعدة البيانات: http://localhost:5000/test-db")
        app.run(debug=True)
        
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("\n🔍 تحقق من:")
    print("1. وجود مجلد eduflow_app")
    print("2. وجود ملف eduflow_app/__init__.py")
    print("3. وجود مكتبات Flask المثبتة")