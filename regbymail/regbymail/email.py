from flask_mail import Message
from . import mail, app

def send_mail(to, subject, template):
    with mail.record_messages() as outbox:
        message = Message(subject, recipients=[to], html=template, \
            sender=app.config['MAIL_DEFAULT_SENDER'])

        mail.send(message)
        return len(outbox) == 1

