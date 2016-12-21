
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from regbymail import db_session

from regbymail.models import User
from regbymail.ldebug import log

class LoginForm(FlaskForm):
    email = TextField(u'email', validators=[DataRequired(), Email()])
    password = PasswordField(u'password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = TextField(u'email', description='Email', validators=[DataRequired(), Email(message=None),Length(min=6, max=40,message='Email length must between 6 and 40')])
    password = PasswordField(u'password', validators=[DataRequired(),Length(min=6, max=25, message='password length must be between 6 and 25')])
    confirm = PasswordField(u'Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])


    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()

        if user:
            self.email.errors.append("Email is already registered!")
            return False
        return True

class ChangePasswordForm(FlaskForm):
    password = PasswordField(u'password', validators=[DataRequired(), Length(min=6, max=26)])
    confirm = PasswordField(u'Repeat password', validators=[DataRequired(), EqualTo('password', message='Password must match')])

class ForgotPasswordForm(FlaskForm):
    email = TextField(u'email', validators=[DataRequired(), Email()])


class ResetPasswordForm(ChangePasswordForm):
    email = HiddenField(u'email', description='Email')
    
    def validate(self):
        log.log('Enter reset password form validate...')
        val = super(ResetPasswordForm, self).validate()
        log.log('Check result {}'.format(val))
        return val     
