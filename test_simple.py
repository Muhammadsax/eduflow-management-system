import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 فحص ملفات المشروع...")

# التحقق من الملفات المهمة
files_to_check = [
    'run.py',
    'config.py',
    'eduflow_app/__init__.py',
    'eduflow_app/forms.py',
    'eduflow_app/models.py',
    'eduflow_app/extensions.py',
    'eduflow_app/auth/__init__.py',
    'eduflow_app/auth/routes.py'
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file} - موجود")
    else:
        print(f"❌ {file} - مفقود")

print("\n📁 محتويات eduflow_app:")
for item in os.listdir('eduflow_app'):
    print(f"  - {item}")

print("\n🎯 جاهز للتشغيل!")