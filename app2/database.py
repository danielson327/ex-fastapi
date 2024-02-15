from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from app2.config import settings
#import psycopg2                  # this is the driver??? that talks to the database allowed us to connect and use sql
#from psycopg2.extras import RealDictCursor
#import time



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)   #i think this is a class so SeesionLocal is an instance

""" SESSION LOCAL IS A CLASS DEF AND EACH INSTANCE IS A DATABASE SESSION  SESSIONMAKER IS A FUNCTIONS
      THE DECLERATIVE BASE FUNCTION RETURNS A CLASS WHICH WE ARE NAMING BASE  USED TO CREATE OUR MOCELS
      IN SESSIONMAKER THE AUTO COMMIT AND AUTOFLUSH ARE BOTH WAYS TO UPDATE THE DATABASE AUTOFLUSH BEING THE ORM METHOD
      BIND = ENGINE  tells the sessionlocal what datase to talk to this line could be instantiated in the __init__ file
       """

Base = declarative_base()    #declarative base is  a fuction that returns a 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#while True:
#    try: 
#        conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user='postgres',password='admin',cursor_factory = RealDictCursor ) 
#        cursor = conn.cursor()
#        print('database connection was successful')
#        break
#    except Exception as error:
#        print('connection to database failed')
#        print('error',error)
#        time.sleep(2)