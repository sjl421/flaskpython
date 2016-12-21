from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def check_confirmed(func):
    @wraps(func)
    def dec_func(*args, **kargs):
        if not current_user.confirmed:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unformed'))
        return func(*args, **kargs)

    return dec_func
