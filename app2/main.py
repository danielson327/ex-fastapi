
#created a virtual enviornment from cmd line: py -3 -m venv venv
# then directed enviornment to use python located within through the view window select python interpreer and supply
# path name .\venv\scripts\python.exe
# to change location in cmd line to virtual env cmd:venv\scripts\activate.bat  --> (venv) c:
#  uvicorn main:app to start server  --reload will enable updates without restarting changed main location to under app so cd app first

from fastapi import FastAPI  #, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import post,user,auth,vote
from . import models 
from app2.database import engine
#from config import settings

#models.Base.metadata.create_all(bind=engine)
"""
metadata.create all must be part of the declerative base set up in database..  this connects to the database and creates all
the tables defined in models... it will add new items but will not update exhisting items need to use
something besides sqlalchemy to do this.

"""



app = FastAPI()

origins = []


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")                   # this is a decorator  also an http get method and the path
def read_root():
    return {"Hello": " World"}







