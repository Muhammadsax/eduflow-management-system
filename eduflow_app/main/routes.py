from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from eduflow_app.main import bp

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    
    context = {
        'user': user,
        'full_name': user.get_full_name(),
        'now': datetime.now(),
        'role_arabic': {
            'student': 'طالب',
            'teacher': 'معلم', 
            'admin': 'مدير النظام'
        }.get(user.role, 'مستخدم')
    }
    
    if user.role == 'student' and hasattr(user, 'student_profile') and user.student_profile:
        context.update({
            'student_id': user.student_profile.student_id,
            'grade': user.student_profile.grade or 'غير محدد',
            'section': user.student_profile.section or 'غير محدد'
        })
    
    elif user.role == 'teacher' and hasattr(user, 'teacher_profile') and user.teacher_profile:
        context.update({
            'teacher_id': user.teacher_profile.teacher_id,
            'department': user.teacher_profile.department or 'غير محدد'
        })
    
    return render_template('main/dashboard.html', **context)

@bp.route('/profile')
@login_required
def profile():
    user = current_user
    context = {
        'user': user,
        'full_name': user.get_full_name(),
        'role_arabic': {
            'student': 'طالب',
            'teacher': 'معلم',
            'admin': 'مدير النظام'
        }.get(user.role, 'مستخدم')
    }
    
    if user.role == 'student' and hasattr(user, 'student_profile') and user.student_profile:
        context['student'] = user.student_profile
    elif user.role == 'teacher' and hasattr(user, 'teacher_profile') and user.teacher_profile:
        context['teacher'] = user.teacher_profile
        
    return render_template('main/profile.html', **context)