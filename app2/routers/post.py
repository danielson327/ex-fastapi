
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session 
from sqlalchemy import func, Select

 
from .. import oauth2
from  app2.database import get_db
from typing import  List, Optional
from .. import models, schemas, utils
from sqlalchemy.orm import with_expression



router = APIRouter( prefix= "/posts", tags = ['Post'])
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current__user),
              limit:int =10, skip:int=0, search: Optional[str] ="" ):     
    #cursor.execute("""SELECT * FROM posts    """)
    #posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    practice = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter = True
    ).group_by(models.Post.id).all()
    results = db.query(models.Post).join(models.Vote,models.Post.id==models.Vote.post_id,isouter = True
    ).group_by(models.Post.id).options(with_expression(models.Post.vote_count, func.count(models.Vote.post_id))).all()
    s=[]
    for row in practice:
        s.append(row._asdict())
        #print(row._asdict())


    #return {"data":posts}  #NEED TO LOOP THROUGH LIST AND SEND OTHERWISE LOOKS WRONG IN MAILMAN 
    return s
@router.get("/{id}",response_model = schemas.Post)  #id is a path parameter always recieved as a string!!!!!
def get_post(id: int, db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current__user)):    #converts id to int or sendes front end an error message
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))         ##INSERT COM1MA AFTER STR(ID),  IF PROBLEMS
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post id {id} was not found")

    #return {"post detail":post}
    return post

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  #changes the default status code to 201
def createpost(post:schemas.PostCreate, db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current__user)):  #Post is our pydantic base class validation and then stored in post
    #cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #print (post.dict())
    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    #return { "data":new_post}
    return new_post
#want a title as string and content as string

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT) 
def delete_posts(id: int,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current__user)):

    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found" )
    #else:
    #   
    #    return Response(status_code=status.HTTP_204_NO_CONTENT)  #in fastapi cannot send anything back but error code
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}",response_model = schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current__user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found" )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    #return {'data':post_query.first()}
    return post_query.first()