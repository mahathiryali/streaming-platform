from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session 
from .database import SessionLocal, engine, Base
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
