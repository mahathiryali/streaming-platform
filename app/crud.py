from sqlalchemy.orm import Session
from . import models, schemas

def get_users(db: Session):
    return db.query(models.User).all()

def process_playback_event(db: Session, event: schemas.ProcessPlaybackEvent):
    existing_state = db.query(models.PlaybackState).filter(
        models.PlaybackState.content_id == event.content_id, models.PlaybackState.user_id == event.user_id).first()
    if existing_state is None:
        new_state = models.PlaybackState(
            user_id = event.user_id,
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
