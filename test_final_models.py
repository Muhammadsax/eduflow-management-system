import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eduflow_app import create_app, db
from eduflow_app.models import User, Student, Teacher

app = create_app()

with app.app_context():
    print("🧪 الاختبار النهائي للنماذج...")
    
    try:
        # تنظيف أي بيانات قديمة
        db.drop_all()
        db.create_all()
        
        # 1. اختبار إنشاء User و Student
        print("1. اختبار User → Student...")
        
        user1 = User(
            username="student_ahmed",
            email="ahmed@eduflow.com",
            first_name="أحمد",
            last_name="علي",
            role="student"
        )
        user1.set_password("password123")
        
        student = Student(
            user=user1,  # هنا نستخدم العلاقة
            student_id="20240001",
            grade="العاشر",
            section="أ",
            parent_name="علي أحمد",
            parent_phone="+966500000001"
        )
        
        db.session.add(user1)
        db.session.commit()
        
        # التحقق من العلاقة
        print(f"   ✅ User Role: {user1.role}")
        print(f"   ✅ Student ID: {user1.student_profile.student_id}")
        print(f"   ✅ العلاقة تعمل: {user1.student_profile.user.username == user1.username}")
        
        # 2. اختبار إنشاء Teacher
        print("\n2. اختبار User → Teacher...")
        
        user2 = User(
            username="teacher_sara",
            email="sara@eduflow.com",
            first_name="سارة",
            last_name="محمد",
            role="teacher"
        )
        user2.set_password("password123")
        
        teacher = Teacher(
            user=user2,
            teacher_id="T001",
            department="الرياضيات",
            qualification="ماجستير في الرياضيات"
        )
        
        db.session.add(user2)
        db.session.commit()
        
        print(f"   ✅ Teacher ID: {user2.teacher_profile.teacher_id}")
        print(f"   ✅ Department: {user2.teacher_profile.department}")
        
        # 3. اختبار الإحصائيات
        print("\n📊 إحصائيات قاعدة البيانات:")
        print(f"   👥 إجمالي المستخدمين: {User.query.count()}")
        print(f"   🎓 عدد الطلاب: {Student.query.count()}")
        print(f"   👨‍🏫 عدد المعلمين: {Teacher.query.count()}")
        
        # 4. اختبار البحث والعلاقات
        print("\n4. اختبار الاستعلامات...")
        
        # البحث عن طالب عبر العلاقة
        student_user = User.query.filter_by(role='student').first()
        if student_user and student_user.student_profile:
            print(f"   ✅ وجدنا الطالب: {student_user.student_profile.student_id}")
        
        # البحث عن معلم عبر العلاقة
        teacher_user = User.query.filter_by(role='teacher').first()
        if teacher_user and teacher_user.teacher_profile:
            print(f"   ✅ وجدنا المعلم: {teacher_user.teacher_profile.teacher_id}")
        
        print("\n🎉 جميع الاختبارات اكتملت بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()