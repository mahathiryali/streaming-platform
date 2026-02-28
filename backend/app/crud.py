from sqlalchemy.orm import Session
from . import models, auth, schemas
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta

def get_users(db: Session):
    return db.query(models.Users).all()

def process_playback_event(db: Session, event, user_id):
    existing_state = db.query(models.PlaybackState).filter(
        models.PlaybackState.content_id == event.content_id, models.PlaybackState.user_id == user_id).first()
    if existing_state is None:
        new_state = models.PlaybackState(
            user_id = user_id,
            content_id = event.content_id,
            device_id = event.device_id,
            session_id = event.session_id,
            position_seconds = event.position_seconds,
            last_event_type = event.event_type,
            last_client_timestamp = event.client_timestamp
            )
        db.add(new_state)
        db.commit()
        db.refresh(new_state)
        return new_state
    else:
        if event.client_timestamp > existing_state.last_client_timestamp:
            existing_state.position_seconds = event.position_seconds
            existing_state.last_event_type = event.event_type
            existing_state.device_id = event.device_id
            existing_state.last_client_timestamp = event.client_timestamp
            existing_state.session_id = event.session_id

            db.commit()
            db.refresh(existing_state)
    
        return existing_state

def get_playback_state(db: Session, user_id: int, content_id: int = None):
    current_users = db.query(models.PlaybackState).filter(
        models.PlaybackState.user_id == user_id
    )
    if content_id is not None:
        current_users = current_users.filter(models.PlaybackState.content_id == content_id)
    
    return current_users.all()

def continue_watching(db: Session, user_id: int):
    results = db.query(models.PlaybackState, models.Content
        ).join(
        models.Content, models.PlaybackState.content_id == models.Content.id
        ).filter(
            models.PlaybackState.user_id == user_id
        ).filter(
            models.PlaybackState.position_seconds > 0   
        ).filter(
            models.PlaybackState.position_seconds < models.Content.duration_seconds
        )

    response = []

    for playback, content in results:
        progress_percent = (playback.position_seconds / content.duration_seconds) * 100

        response.append(schemas.ContinueWatchingItem(
            content_id = content.id,
            title = content.title,
            description = content.description,
            duration_seconds = content.duration_seconds,
            position_seconds = playback.position_seconds,
            progress_percent = round(progress_percent, 2)
            ))

    return response

def authorize_login(db: Session, email: str, password: str):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if auth.verify_password(password, user.hashed_password):
        access_token = auth.create_access_token(
            {"sub": str(user.id)},
            timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
            token_type="access"
        )
        refresh_token = auth.create_access_token(
            {"sub": str(user.id)},
            timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS),
            token_type="refresh"
        )

        expires_at = datetime.now(timezone.utc) + timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
        db_token = models.RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at
        )
        try:
            db.add(db_token)
            db.flush()
        except Exception:
            db.rollback()
            pass

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")

def register_user(db: Session, email: str, password: str):
    existing_user = db.query(models.Users).filter(models.Users.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed = auth.hash_password(password)
    new_user = models.Users(
        email = email,
        created_at = datetime.now(timezone.utc),
        hashed_password = hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = auth.create_access_token(
            {"sub": str(new_user.id)},
            timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
            token_type="access"
    )
    refresh_token = auth.create_access_token(
            {"sub": str(new_user.id)},
            timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS),
            token_type="refresh"
    )

    expires_at = datetime.now(timezone.utc) + timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = models.RefreshToken(
        user_id=new_user.id,
        token=refresh_token,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
    }

def refresh_access_token(db: Session, refresh_token: str):
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    current_time = datetime.now(timezone.utc)
    if db_token.expires_at.tzinfo is None:
        current_time = current_time.replace(tzinfo=None)
    if db_token.expires_at < current_time:
        db.delete(db_token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token"
    )
    payload = auth.decode_token(refresh_token)
    if payload == None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user_id = payload.get("sub")
    if user_id == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token paylod"
        )
    user_id = int(user_id)

    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    db.delete(db_token)
    db.commit()

    new_access_token = auth.create_access_token(
        {"sub": str(user.id)},
        timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )
    new_refresh_token = auth.create_access_token(
        {"sub": str(user.id)},
        timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )

    expires_at = datetime.now(timezone.utc) + timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)

    new_db_token = models.RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=expires_at
    )

    db.add(new_db_token)
    db.commit()
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

def logout_user(db: Session, refresh_token: str):
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    db.delete(db_token)
    db.commit()
    return {"message": "Logged out successfully"}