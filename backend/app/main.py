import openai
from fastapi import FastAPI
from .googlecal.googlecal import read_schedule_from_google

from . import schemas, chatgpt

app = FastAPI()


with open('.openai.key', 'r') as f:
    openai.api_key = f.read()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat", response_model=schemas.Chat)
def post_chat(chat: schemas.ChatPost):

    cal = read_schedule_from_google()
    res = chatgpt.send_chat(chat.message + cal)

    return schemas.Chat(message=chat.message, response=res.choices[0].message.content)