
from flask import render_template, Blueprint, url_for,\
    redirect, flash, request
from flask_login import login_user, logout_user,\
    login_required, current_user

from regbymail.models import User
from regbymail.dbutils import db_session
from regbymail import  bcrypt
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm
from regbymail.token import generate_confirmation_token, confirm_token
from regbymail.email import send_mail

from regbymail.decorators import check_confirmed
import datetime

from regbymail.ldebug import log

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/forgotpassword/', methods=['GET', 'POST'])
def forgotpassword():
    try:
        form = ForgotPasswordForm(request.form)
        if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email=email).first()
            if not user:
                form.email.errors.append('The email:{} is not found!'.format(email))
                return render_template('/user/forgotpassword.html', form=form)
            else:
                print('forgot_pwd.email {}'.format(email))
                token = generate_confirmation_token(email)
                reset_url = url_for('user.reset_password', token=token, _external=True)
                html = render_template('user/reset.html', reset_url=reset_url)
                subject = 'Reset password'
                send_mail(user.email, subject, html)
                flash('An email has been sent to your mailbox.!')
                return render_template('user/unreset.html')
        else: return render_template('user/forgotpassword.html', form=form)
    except:
        log.log_exception()           
            
            
@user_blueprint.route('/resetpassword/<token>')
def reset_password(token):
    try:
        print('Enter forgot_password')
        email = confirm_token(token)
        print('The extract email is:{}'.format(email))
    except:
        log.log_exception()

    try:
        user = User.query.filter_by(email=email).first()
        if user:
            form = ResetPasswordForm()
            form.email.data = user.email
            return render_template('/user/resetpassword.html', form = form)
        else: return 'The User Is Not Found!'
        
    except:
        log.log_exception()

@user_blueprint.route('/applyreset/', methods=['GET', 'POST'])
def apply_reset():
    try:
        print('Enter apply reset logic')
        form = ResetPasswordForm(request.form)
        if form.validate_on_submit():
            print('Reset form data is invalid...')
            email = form.email.data
            user = User.query.filter_by(email=email).first()
            print('email:{0}, password:{1}, confirm:{2}'.format(email, form.password.data, form.confirm.data))
            user.set_password(form.password.data)
            db_session.add(user)
            db_session.commit()
            flash('The password is reset...')
            return redirect(url_for('user.login'))
        else:
            return render_template('/user/resetpassword.html', form=form)
    except:
        log.log_exception()

@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        print('enter confimr_email')
        email = confirm_token(token)
        print('The extract email is: {}'.format(email))
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        log.log_exception()
    
    try:
        user = User.query.filter_by(email=email).first()
    
        if user.confirmed:
            flash('Account already confirmed, Please login.', 'success')
        else:
            user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db_session.add(user)
        db_session.commit()
        flash('Your have confirmed your account. Thanks!', 'Success')
        return redirect(url_for('main.home'))
    except:
        log.log_exception()

@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')

@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    try:
        val_result = form.validate_on_submit()
        log.log('val_result in register is {0}'.format(val_result))
        log.log('request method {0}'.format(request.method))
    except:
        log.log_exception()

    if val_result:
        try:
            log.log('Get post data in register logic')
            user = User(email = form.email.data,
            password = form.password.data, confirmed = False)
            log.log('user email{0}, password{1}'.format(form.email.data, form.password.data))
            db_session.add(user)
            db_session.commit()
            
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('user.confirm_email', token=token, _external=True)
            html = render_template('user/activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email!"
            sendResult = send_mail(user.email, subject, html)
            if sendResult:
                log.log('mail is sent successfully!')
            else:
                log.log('mail is not sent')
            
        except:
            log.log_exception()
        
        try:
            login_user(user)
        except:
            log.log_exception()
        flash('A confirmation email has been sent to your email box.', 'success')
        return redirect(url_for('user.unconfirmed'))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    log.log('enter login')
    try:
        form = LoginForm(request.form)
        log.log('form is got')

        if form.validate_on_submit():
            log.log('login.POST')
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash('Welcome', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Invalid email or password', 'danger')
                return render_template('user/login.html', form=form)
        log.log('Render default login.form')
        return render_template('user/login.html', form=form)
    except BaseException:
        log.log_exception()


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))

@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile():
    try:
        form = ChangePasswordForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=current_user.email).first()
            if user:
                user.password = bcrypt.generate_password_hash(form.password.data)
                db_session.commit()
                flash('Password successfully changed', 'success')
                return redirect(url_for('user.profile'))
            else:
                flash('Unable to change the password', 'danger')
                return redirect(url_for('user.profile'))
        return render_template('user/profile.html', form=form)
    except:
        log.log_exception()

@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    try:
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject="Please confirm your email"
        send_mail(current_user.email, subject, html)
        flash('A new confirmation email has been send.', 'success')
        return redirect(url_for('user.unconfirmed'))
    except:
        log.log_exception()

