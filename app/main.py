from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session 
from .database import SessionLocal, engine, Base
from typing import List
from . import models, crud, schemas


Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 

@app.post("/playback/event", response_model=schemas.PlaybackStateResponse)
def handle_event(event: schemas.ProcessPlaybackEvent, db: Session = Depends(get_db)):
    return crud.process_playback_event(db, event)

@app.get("/playback/state", response_model=List[schemas.PlaybackStateResponse])
def get_state(user_id: int, content_id: int = Query(None), db: Session = Depends(get_db)):
    return crud.get_playback_state(db, user_id, content_id)

@app.get("users/{user_id}/continue_watching", response_model=List[schemas.ContinueWatchingItem])
def get_continue_watching(user_id: int, db: Session = Depends(get_db)):
    return crud.continue_watching(db, user_id)