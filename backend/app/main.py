import openai
from fastapi import FastAPI

from . import schemas, chatgpt

app = FastAPI()


with open('.openai.key', 'r') as f:
    openai.api_key = f.read()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat", response_model=schemas.Chat)
def post_chat(chat: schemas.ChatPost):
    res = chatgpt.send_chat(chat.message)