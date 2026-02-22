import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ── User ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    login: str
    last_visit: datetime | None = None


class UserUpdate(BaseModel):
    login: str | None = None
    last_visit: datetime | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    last_visit: datetime | None


# ── Group ─────────────────────────────────────────────────────────────────────

class GroupCreate(BaseModel):
    name: str
    user_id: int


class GroupUpdate(BaseModel):
    name: str | None = None


class GroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    user_id: int


# ── LearningCard ──────────────────────────────────────────────────────────────

class LearningCardCreate(BaseModel):
    name: str
    source_url: str | None = None
    schedule: str | None = None
    tg_chat_id: str | None = None
    tg_topic_id: int | None = None
    message_template: str | None = None
    group_id: int | None = None
    is_active: bool = True
    user_id: int


class LearningCardUpdate(BaseModel):
    name: str | None = None
    source_url: str | None = None
    schedule: str | None = None
    tg_chat_id: str | None = None
    tg_topic_id: int | None = None
    message_template: str | None = None
    group_id: int | None = None
    is_active: bool | None = None


class LearningCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    source_url: str | None
    schedule: str | None
    tg_chat_id: str | None
    tg_topic_id: int | None
    message_template: str | None
    group_id: int | None
    is_active: bool
    add_date: datetime
    user_id: int


# ── Newsletter ────────────────────────────────────────────────────────────────

class NewsletterCreate(BaseModel):
    user_id: int
    learning_card_id: uuid.UUID
    send_date: datetime


class NewsletterUpdate(BaseModel):
    send_date: datetime | None = None


class NewsletterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    learning_card_id: uuid.UUID
    send_date: datetime
