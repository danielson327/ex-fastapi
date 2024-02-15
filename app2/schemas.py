


from typing import Optional
from pydantic import BaseModel, EmailStr ,conint  #helps validate data...python library not fastapi
from datetime import datetime

class PostBase(BaseModel):                  #this is a pydantic class for vetting front end data
    title:str
    content:str
    published: bool = True
    class config:
        orm_model = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        orm_model=True
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    owner: UserOut

    
    class Config:
        from_attributes = True
        orm_model=True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
   
 
class Vote(BaseModel):
    post_id:int
    dir : int

class PostOut(BaseModel):
    Post: Post
    votes: int
    class configure:
        
        orm_mode = True



