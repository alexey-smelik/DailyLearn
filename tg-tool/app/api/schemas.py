from pydantic import BaseModel


class SendRequest(BaseModel):
    tg_chat_id: str
    tg_topic_id: int | None = None
    card_id: str
    card_name: str
    source_url: str | None = None
    schedule: str | None = None
    message_template: str | None = None
    show_pause_button: bool = True
    show_skip_button: bool = True
    show_quiz_button: bool = False
    has_conspect: bool = False


class SendResponse(BaseModel):
    ok: bool


class ConspectRequestBody(BaseModel):
    tg_chat_id: str
    tg_topic_id: int | None = None
    card_id: str
    card_name: str
    time_to_educate: str | None = None
