
from flask import render_template, Blueprint, url_for,\
    redirect, flash, request
from flask_login import login_user, logout_user,\
    login_required, current_user

from regbymail.models import User
from regbymail import session, bcrypt
from .forms import LoginForm, RegisterForm, ChangePasswordForm

from regbymail.ldebug import log

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register', methods=['GET', 'POST'])
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
            password = form.password.data)
            log.log('user email{0}, password{1}'.format(form.email.data, form.password.data))
            session.add(user)
            session.commit()
        except:
            log.log_exception()
        
        try:
            login_user(user)
        except:
            log.log_exception()
        flash('You registered and are now logged in. Welcome!', 'success')
        return redirect(url_for('main.home'))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    log.log('enter login')
    try:
        form = LoginForm(request.form)
        log.log('form is got')

        if form.validate_on_submit():
            log.log('login.POST')
            user = session.query(User).filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash('Welcome', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Invalid email and/ or password', 'danger')
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
def profile():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            session.commit()
            flash('Password successfully changed', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Unable to change the password', 'danger')
            return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)
    
