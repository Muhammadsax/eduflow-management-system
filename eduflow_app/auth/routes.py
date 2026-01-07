from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from eduflow_app.auth import bp
from eduflow_app.forms import LoginForm, RegistrationForm
from eduflow_app.models import User, Student, Teacher
from eduflow_app.extensions import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    # إذا كان المستخدم مسجلاً بالفعل، توجيهه للصفحة الرئيسية
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # البحث عن المستخدم بالبريد الإلكتروني
        user = User.query.filter_by(email=form.email.data).first()
        
        # التحقق من وجود المستخدم وصحة كلمة المرور
        if user is None or not user.check_password(form.password.data):
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))
        
        # التحقق من أن الحساب مفعل
        if not user.is_active:
            flash('حسابك معطل، الرجاء التواصل مع الإدارة', 'warning')
            return redirect(url_for('auth.login'))
        
        # تسجيل دخول المستخدم
        login_user(user, remember=form.remember_me.data)
        
        # تحديث وقت آخر زيارة
        user.last_seen = db.func.now()
        db.session.commit()
        
        flash(f'مرحباً بعودتك {user.first_name}!', 'success')
        
        # التوجيه للصفحة التالية أو الرئيسية
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', title='تسجيل الدخول', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """صفحة تسجيل حساب جديد"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # إنشاء مستخدم جديد
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        # حفظ المستخدم في قاعدة البيانات
        db.session.add(user)
        db.session.commit()
        
        # بناءً على الدور، إنشاء ملف خاص
        if form.role.data == 'student':
            student = Student(
                user_id=user.id,
                student_id=f"S{user.id:06d}",  # إنشاء رقم طالب تلقائي
                grade="غير محدد",
                section="غير محدد"
            )
            db.session.add(student)
        elif form.role.data == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                teacher_id=f"T{user.id:06d}",  # إنشاء رقم معلم تلقائي
                department="غير محدد"
            )
            db.session.add(teacher)
        
        db.session.commit()
        
        # تسجيل دخول تلقائي بعد التسجيل
        login_user(user)
        
        flash('تم إنشاء حسابك بنجاح! مرحباً بك في EduFlow', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', title='تسجيل حساب جديد', form=form)

@bp.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('main.index'))