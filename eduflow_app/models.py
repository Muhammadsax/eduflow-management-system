from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='student')  # student, teacher, admin
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

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
    student_id = db.Column(db.String(20), unique=True)  # رقم الطالب
    grade = db.Column(db.String(20))  # الصف
    section = db.Column(db.String(20))  # القسم
    enrollment_date = db.Column(db.Date)
    parent_name = db.Column(db.String(128))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))

    # العلاقة العكسية: من User إلى Student (واحد لواحد) تم تعريفها في User

    # علاقة واحدة لكثير: طالب لديه عدة درجات
    grades = db.relationship('Grade', backref='student', lazy=True, cascade="all, delete-orphan")

    # علاقة واحدة لكثير: طالب لديه عدة مدفوعات
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

    # العلاقة العكسية: من User إلى Teacher (واحد لواحد) تم تعريفها في User

    # علاقة واحدة لكثير: معلم يقوم بتدريس عدة كورسات
    courses = db.relationship('Course', backref='teacher', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Teacher {self.teacher_id}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    # علاقة واحدة لكثير: كورس لديه عدة درجات (لعدة طلاب)
    grades = db.relationship('Grade', backref='course', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course {self.course_code}>'


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade = db.Column(db.String(2))  # مثل A, B+, etc.
    score = db.Column(db.Float)  # النسبة المئوية
    semester = db.Column(db.String(20))
    year = db.Column(db.Integer)

    # نريد أن يكون لكل طالب في كل كورس درجة واحدة فقط، لذلك نصنع constraint فريد
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),)

    def __repr__(self):
        return f'<Grade {self.grade} for Student {self.student_id} in Course {self.course_id}>'


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))
    description = db.Column(db.String(200))
    is_paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Payment {self.id} for Student {self.student_id}>'


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20), unique=True)
    category = db.Column(db.String(50))
    file_path = db.Column(db.String(500))  # المسار إلى الملف المرفوع
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title}>'