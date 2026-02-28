from http.client import HTTPException
from fastapi import FastAPI, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from app.database import engine, Base
from typing import List
from app import models, crud, schemas, database
from app.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/users/me", response_model=schemas.RegisterRequest)
def get_me(current_user: models.Users = Depends(get_current_user)):
    return {"email": current_user.email, "password": "hidden"}

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
def login_user(db: Session = Depends(database.get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authorize_login(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.post("/auth/register", response_model=schemas.LoginItem)
def register_user(request: schemas.RegisterRequest, db: Session = Depends(database.get_db)):
    return crud.register_user(db, request.email, request.password)

@app.post("/auth/refresh", response_model=schemas.LoginItem)
def refresh_user_token(refresh: schemas.RefreshTokenRequest, db: Session = Depends(database.get_db)):
    return crud.refresh_access_token(db, refresh.refresh_token)

@app.post("/auth/logout")
def logout_user(refresh: schemas.RefreshTokenRequest, db: Session = Depends(database.get_db)):
    return crud.logout_user(db, refresh.refresh_token)