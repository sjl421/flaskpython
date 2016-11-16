# coding=utf-8
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object('config')

# Connect to mysql
con_str = app.config['SQLALCHEMY_DATABASE_URI']
print(con_str)
engine = create_engine(con_str, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
print('session is alive')
from sqlch import views


