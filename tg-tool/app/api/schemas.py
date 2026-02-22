from pydantic import BaseModel


class SendRequest(BaseModel):
    tg_chat_id: str
    tg_topic_id: int | None = None
    card_id: str
    card_name: str
    source_url: str | None = None
    schedule: str | None = None
    message_template: str | None = None


class SendResponse(BaseModel):
    ok: bool
