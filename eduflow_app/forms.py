from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from eduflow_app.models import User

class LoginForm(FlaskForm):
    """نموذج تسجيل الدخول"""
    email = StringField('البريد الإلكتروني', validators=[
        DataRequired(message='حقل البريد الإلكتروني مطلوب'),
        Email(message='بريد إلكتروني غير صحيح')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired(message='كلمة المرور مطلوبة'),
        Length(min=6, message='كلمة المرور يجب أن تكون 6 أحرف على الأقل')
    ])
    remember_me = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')

class RegistrationForm(FlaskForm):
    """نموذج تسجيل مستخدم جديد"""
    username = StringField('اسم المستخدم', validators=[
        DataRequired(message='اسم المستخدم مطلوب'),
        Length(min=3, max=64, message='اسم المستخدم يجب أن يكون بين 3 و 64 حرف')
    ])
    email = StringField('البريد الإلكتروني', validators=[
        DataRequired(message='البريد الإلكتروني مطلوب'),
        Email(message='بريد إلكتروني غير صحيح')
    ])
    first_name = StringField('الاسم الأول', validators=[
        DataRequired(message='الاسم الأول مطلوب')
    ])
    last_name = StringField('اسم العائلة', validators=[
        DataRequired(message='اسم العائلة مطلوب')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired(message='كلمة المرور مطلوبة'),
        Length(min=6, message='كلمة المرور يجب أن تكون 6 أحرف على الأقل')
    ])
    password2 = PasswordField('تأكيد كلمة المرور', validators=[
        DataRequired(message='تأكيد كلمة المرور مطلوب'),
        EqualTo('password', message='كلمتا المرور غير متطابقتين')
    ])
    role = SelectField('الدور', choices=[
        ('student', 'طالب'),
        ('teacher', 'معلم'),
        ('admin', 'مدير النظام')
    ], validators=[DataRequired()])
    submit = SubmitField('تسجيل حساب جديد')
    
    def validate_username(self, username):
        """التحقق من أن اسم المستخدم غير مستخدم"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('اسم المستخدم مستخدم مسبقاً، الرجاء اختيار اسم آخر.')
    
    def validate_email(self, email):
        """التحقق من أن البريد الإلكتروني غير مستخدم"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('البريد الإلكتروني مستخدم مسبقاً، الرجاء استخدام بريد آخر.')