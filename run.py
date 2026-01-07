import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eduflow_app import create_app

app = create_app()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EduFlow - نظام إدارة التعليم</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --primary: #667eea;
                --secondary: #764ba2;
                --success: #28a745;
                --warning: #ffc107;
                --info: #17a2b8;
            }
            body {
                background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', 'Tahoma', Geneva, Verdana, sans-serif;
            }
            .welcome-container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 50px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
                max-width: 800px;
                text-align: center;
            }
            .logo-main {
                font-size: 4rem;
                color: var(--primary);
                margin-bottom: 20px;
            }
            .feature-list {
                text-align: right;
                margin: 30px 0;
            }
            .feature-item {
                padding: 10px 0;
                border-bottom: 1px solid #eee;
                font-size: 1.1rem;
            }
            .tech-badge {
                background: linear-gradient(45deg, var(--primary), var(--secondary));
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
                margin: 0 5px;
            }
        </style>
    </head>
    <body>
        <div class="welcome-container">
            <div class="logo-main">
                <i class="fas fa-graduation-cap"></i>
            </div>
            
            <h1 class="display-4 mb-3" style="color: var(--primary);">مرحباً بكم في EduFlow</h1>
            <p class="lead mb-4">نظام إدارة التعليم المتكامل للطلاب والمعلمين والإدارة</p>
            
            <div class="feature-list">
                <div class="feature-item">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    نظام شؤون الطلاب الأكاديمية
                </div>
                <div class="feature-item">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    مكتبة إلكترونية متكاملة
                </div>
                <div class="feature-item">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    منتدى تعليمي تفاعلي
                </div>
                <div class="feature-item">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    نظام مراسلات مع أولياء الأمور
                </div>
                <div class="feature-item">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    إدارة المدفوعات والرسوم الدراسية
                </div>
            </div>
            
            <div class="d-flex justify-content-center gap-3 my-4">
                <a href="/auth/login" class="btn btn-primary btn-lg px-5">
                    <i class="fas fa-sign-in-alt me-2"></i>تسجيل الدخول
                </a>
                <a href="/auth/register" class="btn btn-outline-primary btn-lg px-5">
                    <i class="fas fa-user-plus me-2"></i>إنشاء حساب جديد
                </a>
            </div>
            
            <div class="mt-4">
                <p class="text-muted mb-2">مبني بتقنيات:</p>
                <div>
                    <span class="tech-badge">Flask</span>
                    <span class="tech-badge">SQLAlchemy</span>
                    <span class="tech-badge">Bootstrap 5</span>
                    <span class="tech-badge">Jinja2</span>
                </div>
            </div>
            
            <div class="mt-4 text-muted">
                <small>© 2024 EduFlow - جميع الحقوق محفوظة</small>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 تشغيل نظام EduFlow لإدارة التعليم")
    print("=" * 60)
    print("📌 الواجهة الرئيسية: http://localhost:5000")
    print("🔐 تسجيل الدخول:     http://localhost:5000/auth/login")
    print("📝 إنشاء حساب:       http://localhost:5000/auth/register")
    print("📊 لوحة التحكم:      http://localhost:5000/dashboard")
    print("=" * 60)
    print("⚡ Debug Mode: ON")
    print("📁 Working Directory:", os.getcwd())
    print("=" * 60)
    
    app.run(debug=True, port=5000)