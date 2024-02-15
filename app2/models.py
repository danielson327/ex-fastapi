

from app2.database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship 
from sqlalchemy.orm import query_expression

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key = True,nullable = False)
    title = Column(String, nullable = False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default= 'True', nullable = False)    #the databasese is setting the default server default
    created_at= Column(TIMESTAMP(timezone=True), nullable = False,  server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    
    owner = relationship('User')
    vote_count = query_expression()

       
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True,nullable = False)
    email = Column(String, nullable = False, unique= True)
    password = Column(String, nullable = False)
    created_at= Column(TIMESTAMP(timezone=True), nullable = False,  server_default=text('now()'))

class Vote(Base):
    __tablename__='votes'
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
