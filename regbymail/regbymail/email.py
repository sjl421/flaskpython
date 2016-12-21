from flask_mail import Message
from . import mail, app

def send_mail(to, subject, template):
    message = Message(subject, recipients=[to], html=template, \
        sender=app.config['MAIL_DEFAULT_SENDER'])

    mail.send(message)

