
from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

#user_credentials: OAuth2PasswordRequestForm = Depends()  this defines user_cred as type OAuth and dep() makes an instance of OAuth,(shorcut notation)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db )):
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data= {"user_id":user.id})
    
    return {"access_token": access_token,"token_type":"bearer"}     #bearer is handled on the front end????? this is the required return format

