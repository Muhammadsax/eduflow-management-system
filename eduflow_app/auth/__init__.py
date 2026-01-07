from flask import Blueprint

# إنشاء Blueprint للمصادقة
bp = Blueprint('auth', __name__)

# استيراد المسارات
from eduflow_app.auth import routes