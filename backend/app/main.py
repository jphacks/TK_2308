import openai
from fastapi import FastAPI

from . import schemas, chatgpt, slack

app = FastAPI()


with open('.openai.key', 'r') as f:
    openai.api_key = f.read()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat", response_model=schemas.Chat)
def post_chat(chat: schemas.ChatPost):
    res = chatgpt.send_chat(chat.message)

    return schemas.Chat(message=chat.message, response=res.choices[0].message.content)


@app.post("/post", response_model=schemas.Message)
def post_chat(message: schemas.MessagePost):
    res = slack.post_message(message.message)

    ok = res is not None
    return schemas.Message(ok=ok)