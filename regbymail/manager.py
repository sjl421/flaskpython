from regbymail.models import User
from regbymail import app
from regbymail.dbutils import Base, DBEngine, db_session
from flask_script import Manager

manager = Manager(app)

@manager.command
def run():
    app.run(host="0.0.0.0", port=8080)

@manager.command
def init_db():
   Base.metadata.create_all(DBEngine)

@manager.command
def del_testdata():
    users = User.query.filter(User.email.startswith('rainychan@'))
    for user in users:
        db_session.delete(user)
        db_session.commit()
    print('Operation is complete. Success!')

def main():
    manager.run()

if __name__ == '__main__':
    main()
