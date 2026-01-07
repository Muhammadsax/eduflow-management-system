from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='student')
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # علاقة واحدة لواحدة مع Student
    student_profile = db.relationship('Student', backref='user', uselist=False, cascade="all, delete-orphan")

    # علاقة واحدة لواحدة مع Teacher
    teacher_profile = db.relationship('Teacher', backref='user', uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True)
    grade = db.Column(db.String(20))
    section = db.Column(db.String(20))
    enrollment_date = db.Column(db.Date)
    parent_name = db.Column(db.String(128))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))

    # ❌ احذف هذا السطر (تم تعريفه في User كـ backref):
    # user = db.relationship('User', backref=db.backref('student_profile', uselist=False))

    # علاقة واحدة لكثير
    grades = db.relationship('Grade', backref='student', lazy=True, cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='student', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Student {self.student_id}>'


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.String(20), unique=True)
    department = db.Column(db.String(64))
    hire_date = db.Column(db.Date)
    qualification = db.Column(db.Text)

    # ❌ احذف هذا السطر (تم تعريفه في User كـ backref):
    # user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False))
    
    # علاقة واحدة لكثير
    courses = db.relationship('Course', backref='teacher', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Teacher {self.teacher_id}>'


# ... باقي النماذج تبقى كما هي ...

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    grades = db.relationship('Grade', backref='course', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course {self.course_code}>'


# ... باقي النماذج تبقى كما هي ...

# ⭐⭐⭐ دالة user_loader للـ Flask-Login ⭐⭐⭐
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))