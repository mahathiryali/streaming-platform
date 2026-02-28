from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class ProcessPlaybackEvent(BaseModel):
    content_id: int
    event_type: str
    position_seconds: int
    client_timestamp: datetime
    device_id: str
    session_id: UUID

    model_config = ConfigDict(from_attributes=True)

class PlaybackStateResponse(BaseModel):
    user_id: int
    content_id: int
    device_id: str
    session_id: UUID
    position_seconds: int
    last_event_type: str
    last_client_timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ContinueWatchingItem(BaseModel):
    content_id: int
    title: str
    description: str
    duration_seconds: int
    position_seconds: int
    progress_percent: float

    model_config = ConfigDict(from_attributes=True)

class LoginItem(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RegisterRequest(BaseModel):
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str