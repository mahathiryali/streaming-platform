from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session 
from .database import SessionLocal, engine 
from . import models, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/playback/event")
def playback_event(event):
    return {}

def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 

@app.get("/users") 
def read_users(db: Session = Depends(get_db)): 
    return crud.get_users(db)