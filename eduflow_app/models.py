from datetime import datetime
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db , login_manager


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
    
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    
    def set_password(self, password):
        """تشفير كلمة المرور وحفظها"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """التحقق من كلمة المرور"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """الحصول على الاسم الكامل"""
        return f"{self.first_name} {self.last_name}"

    # علاقة واحدة لواحدة مع Student
    student_profile = db.relationship('Student', back_populates='user', uselist=False, cascade="all, delete-orphan")

    # علاقة واحدة لواحدة مع Teacher
    teacher_profile = db.relationship('Teacher', backref='user', uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.username}>'
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='student_profile')
    student_id = db.Column(db.String(20), unique=True)  # رقم الطالب
    grade = db.Column(db.String(20))  # الصف
    section = db.Column(db.String(20))  # القسم
    enrollment_date = db.Column(db.Date)
    parent_name = db.Column(db.String(128))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))

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
    user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False))
    
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
    credit_hours = db.Column(db.Integer, default=3)  # ساعات معتمدة
    semester = db.Column(db.String(20))  # فصل دراسي
    year = db.Column(db.Integer)  # السنة الدراسية
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    
    # إضافة علاقة مع Enrollment
    enrollments = db.relationship('Enrollment', backref='course_enrollments', lazy=True, cascade="all, delete-orphan")
    
    # علاقة واحدة لكثير: كورس لديه عدة درجات (لعدة طلاب)
    grades = db.relationship('Grade', backref='course', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course {self.course_code}>'    __tablename__ = 'courses'

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
    
class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_pinned = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    
    # العلاقات
    user = db.relationship('User', backref='forum_posts')
    comments = db.relationship('ForumComment', backref='post', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<ForumPost {self.title[:30]}...>'
    
class ForumComment(db.Model):
    __tablename__ = 'forum_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('forum_comments.id'), nullable=True)  # للردود المتداخلة
    
    # العلاقات
    user = db.relationship('User', backref='forum_comments')
    replies = db.relationship('ForumComment', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    def __repr__(self):
        return f'<ForumComment by User:{self.user_id} on Post:{self.post_id}>'
    
class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)
    is_urgent = db.Column(db.Boolean, default=False)
    
    # العلاقات
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id}>'
    
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50))  # grade, payment, message, forum, etc.
    related_id = db.Column(db.Integer)  # ID of related item (grade_id, message_id, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    # العلاقة
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification for User:{self.user_id} - {self.title[:30]}...>'
    
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    
    # لمنع التسجيل المزدوج
    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),
    )
    
    # العلاقات
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')
    
    def __repr__(self):
        return f'<Enrollment Student:{self.student_id} in Course:{self.course_id}>'
# هذه الدالة مطلوبة لـ Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))