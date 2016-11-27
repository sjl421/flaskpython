
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from regbymail import session

from regbymail.models import User

class LoginForm(FlaskForm):
    email = TextField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = TextField('email', validators=[DataRequired(), Email(message='Please input a valid email address'),Length(min=6, max=40,message='Email length must between 6 and 40')])
    password = PasswordField('password', validators=[DataRequired(),Length(min=6, max=25, message='password length must be between 6 and 25')])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])


    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = session.query(User).filter_by(email=self.email.data).first()

        if user:
            self.email.errors.append("Email is already registered!")
            return False
        return True

class ChangePasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=26)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Password must match')])

    
