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
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: white;
            }
            .welcome-card {
                background: rgba(255,255,255,0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 600px;
                color: #333;
            }
            .logo {
                font-size: 3em;
                color: #667eea;
                margin-bottom: 20px;
            }
            .btn-primary {
                background: #667eea;
                border: none;
                padding: 12px 30px;
                font-size: 1.1em;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="welcome-card">
            <div class="logo">
                <i class="fas fa-graduation-cap"></i> EduFlow
            </div>
            <h1 class="mb-4">نظام إدارة التعليم المتكامل</h1>
            <p class="lead mb-4">منصة متكاملة لإدارة العملية التعليمية</p>
            
            <div class="mb-4">
                <a href="/auth/login" class="btn btn-primary">
                    <i class="fas fa-sign-in-alt"></i> تسجيل الدخول
                </a>
                <a href="/auth/register" class="btn btn-outline-primary">
                    <i class="fas fa-user-plus"></i> إنشاء حساب جديد
                </a>
            </div>
            
        </div>
        
        <!-- Font Awesome -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 تشغيل EduFlow على http://localhost:5000")
    print("🔐 صفحة تسجيل الدخول: http://localhost:5000/auth/login")
    print("📝 صفحة التسجيل: http://localhost:5000/auth/register")
    app.run(debug=True, port=5000)