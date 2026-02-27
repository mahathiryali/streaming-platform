from fastapi import FastAPI, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from .database import SessionLocal, engine, Base
from typing import List
from . import models, crud, schemas, database
from .dependencies import get_current_user


Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/playback/event", response_model=schemas.PlaybackStateResponse)
def handle_event(event: schemas.ProcessPlaybackEvent, current_user = Depends(get_current_user), db: Session = Depends(database.get_db)):
    return crud.process_playback_event(db, event, current_user.id)

@app.get("/playback/state", response_model=List[schemas.PlaybackStateResponse])
def get_state(current_user: models.Users = Depends(get_current_user), content_id: int = Query(None), db: Session = Depends(database.get_db)):
    return crud.get_playback_state(db, current_user.id, content_id)

@app.get("/users/me/continue_watching", response_model=List[schemas.ContinueWatchingItem])
def get_continue_watching(current_user: models.Users = Depends(get_current_user), db: Session = Depends(database.get_db)):
    return crud.continue_watching(db, current_user.id)

@app.post("/auth/login", response_model=schemas.LoginItem)
def get_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return crud.authorize_login(db, form_data.username, form_data.password)

@app.post("/auth/register", response_model=schemas.LoginItem)
def register_user(form_data: schemas.RegisterRequest, db: Session = Depends(database.get_db)):
    return crud.register_user(db, form_data.email, form_data.password)