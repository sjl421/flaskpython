from regbymail.models import User
from regbymail import app
from regbymail.dbutils import Base, DBEngine
from flask_script import Manager

manager = Manager(app)

@manager.command
def run():
    app.run(host="0.0.0.0", port=8080)

@manager.command
def init_db():
   Base.metadata.create_all(DBEngine)

def main():
    manager.run()

if __name__ == '__main__':
    main()
