# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#import database base model
from sqlalchemy.ext.declarative import declarative_base

def get_db_session(connectionstr):
    engine = create_engine(connectionstr, echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def get_db_base():
    Base = declarative_base()
    return Base
