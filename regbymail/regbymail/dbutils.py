# coding=utf-8

from regbymail import connectionstr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

#import database base model
from sqlalchemy.ext.declarative import declarative_base

DBEngine = create_engine(connectionstr, echo=False)
    #Session = sessionmaker()
    #Session.configure(bind=engine)
    #session = Session()
    
    # To follow the official doc.
db_session = scoped_session(sessionmaker(autocommit=False, \
    autoflush=False, bind=DBEngine)) 

Base = declarative_base()

#create werzeug instance
Base.query = db_session.query_property()

