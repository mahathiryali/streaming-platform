from sqlalchemy import Column, Integer, String, BIGINT, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class PlaybackState(Base):
    __tablename__ = "playback_state"

    __table_args__ = (
        UniqueConstraint("user_id", "content_id", name="unique_user_content"),
    )

    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, nullable=False, index=True)
    content_id = Column(BIGINT, nullable=False, index=True)
    device_id = Column(String, nullable=False)
    session_id = Column(UUID(as_uuid=True), nullable=False)
    position_seconds = Column(Integer, nullable=False)
    last_event_type = Column(String, nullable=False)
    last_client_timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class Users(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, index=True)
    email = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class Content(Base):
    __tablename__ = "content"

    id = Column(BIGINT, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class WatchEvent(Base):
    __tablename__ = "watch_events"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False, index=True)
    content_id = Column(BIGINT, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    position_seconds = Column(Integer, nullable=False)
    client_timestamp = Column(TIMESTAMP(timezone=True), nullable=False)