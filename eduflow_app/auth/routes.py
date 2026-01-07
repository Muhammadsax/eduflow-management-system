from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse  # ✅ تم التغيير هنا
from eduflow_app.auth import bp
from eduflow_app.forms import LoginForm, RegistrationForm
from eduflow_app.models import User, Student, Teacher
from eduflow_app.extensions import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('حسابك معطل، الرجاء التواصل مع الإدارة', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        user.last_seen = db.func.now()
        db.session.commit()
        
        flash(f'مرحباً بعودتك {user.first_name}!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':  # ✅ تم التغيير هنا
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
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        if form.role.data == 'student':
            student = Student(
                user_id=user.id,
                student_id=f"S{user.id:06d}",
                grade="غير محدد",
                section="غير محدد"
            )
            db.session.add(student)
        elif form.role.data == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                teacher_id=f"T{user.id:06d}",
                department="غير محدد"
            )
            db.session.add(teacher)
        
        db.session.commit()
        
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