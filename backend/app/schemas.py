from pydantic import BaseModel


class ChatBase(BaseModel):
    message: str

    # DB 保存用クラスといい感じに相互変換するようにしてねとお願いする
    class Config:
        orm_mode = True


class ChatPost(ChatBase):
    pass


class Chat(ChatBase):
    response: str


class MessageBase(BaseModel):
    class Config:
        orm_mode = True


class MessagePost(MessageBase):
    message: str


class Message(MessageBase):
    ok: bool


class SlackEvent(BaseModel):
    type: str
    challenge: str = None
    event: dict = None


class SummarizeBase(BaseModel):
    from_date: str
    to_date: str
    channel_name: str

    class Config:
        orm_mode = True


class SummarizePost(SummarizeBase):
    pass


class SummarizeResult(SummarizeBase):
    summary: str
