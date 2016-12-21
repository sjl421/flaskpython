from itsdangerous import URLSafeTimedSerializer
from . import app

_sk = app.config['SECRET_KEY']
_sps = app.config['SECURITY_PASSWORD_SALT']

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(_sk)
    return serializer.dumps(email, salt = _sps)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(_sk)
    try:
        email = serializer.loads(token, salt = _sps, max_age = expiration)
    except:
        return False
    return email
