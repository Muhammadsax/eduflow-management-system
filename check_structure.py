import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 فحص هيكل المشروع...")

# فحص ملفات مهمة
files = [
    'run.py',
    'config.py',
    'eduflow_app/__init__.py',
    'eduflow_app/models.py',
    'eduflow_app/forms.py',
    'eduflow_app/extensions.py',
    'eduflow_app/auth/__init__.py',
    'eduflow_app/auth/routes.py',
    'eduflow_app/main/__init__.py',
    'eduflow_app/main/routes.py'
]

for file in files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - مفقود")

# فحص الوحدات
print("\n📁 محتويات eduflow_app:")
for item in os.listdir('eduflow_app'):
    if os.path.isdir(f"eduflow_app/{item}"):
        print(f"  📂 {item}/")
        # عرض محتويات المجلدات المهمة
        if item in ['auth', 'main']:
            for sub in os.listdir(f"eduflow_app/{item}"):
                print(f"    📄 {sub}")
    else:
        print(f"  📄 {item}")

print("\n🎯 جاهز للتشغيل!")