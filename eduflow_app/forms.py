from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from eduflow_app.models import User

class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[
        DataRequired('حقل البريد الإلكتروني مطلوب'),
        Email('بريد إلكتروني غير صحيح')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired('كلمة المرور مطلوبة'),
        Length(min=6, message='كلمة المرور يجب أن تكون 6 أحرف على الأقل')
    ])
    remember_me = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')

class RegistrationForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[
        DataRequired('اسم المستخدم مطلوب'),
        Length(min=3, max=64, message='اسم المستخدم يجب أن يكون بين 3 و 64 حرف')
    ])
    email = StringField('البريد الإلكتروني', validators=[
        DataRequired('البريد الإلكتروني مطلوب'),
        Email('بريد إلكتروني غير صحيح')
    ])
    first_name = StringField('الاسم الأول', validators=[DataRequired('الاسم الأول مطلوب')])
    last_name = StringField('اسم العائلة', validators=[DataRequired('اسم العائلة مطلوب')])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired('كلمة المرور مطلوبة'),
        Length(min=6, message='كلمة المرور يجب أن تكون 6 أحرف على الأقل')
    ])
    password2 = PasswordField('تأكيد كلمة المرور', validators=[
        DataRequired('تأكيد كلمة المرور مطلوب'),
        EqualTo('password', 'كلمتا المرور غير متطابقتين')
    ])
    role = SelectField('الدور', choices=[
        ('student', 'طالب'),
        ('teacher', 'معلم'),
        ('admin', 'مدير النظام')
    ])
    submit = SubmitField('تسجيل حساب جديد')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('اسم المستخدم مستخدم مسبقاً')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('البريد الإلكتروني مستخدم مسبقاً')