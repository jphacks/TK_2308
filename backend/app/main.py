import openai
from .googlecal.googlecal import read_schedule_from_google
from fastapi import FastAPI, Depends, HTTPException, Request

from . import schemas, chatgpt

app = FastAPI()


with open(".openai.key", "r") as f:
    openai.api_key = f.read()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat", response_model=schemas.Chat)
def post_chat(chat: schemas.ChatPost):

    cal = read_schedule_from_google()
    schedules_str = ','.join(str(item) for item in cal)

    message_str = f"「相手のメッセージ：{chat.message}」「自分のスケジュール：{schedules_str}」"

    res = chatgpt.send_chat(message_str)

    return schemas.Chat(message=chat.message, response=res.choices[0].message.content)


@app.post("/slack/events")
async def slack_events(request: Request, slack_event: schemas.SlackEvent):
    body = await request.body()
    headers = request.headers
    print(body, headers)
    if not slack.verify_signature(body, headers):
        raise HTTPException(status_code=400, detail="Invalid request or signature")
    print("signature ok")

    # URL 認証のための challenge 応答
    if slack.is_verification(slack_event.type):
        print("sending back the challenge")
        return {"challenge": slack_event.challenge}

    # メッセージイベントに応答

    if not slack.is_callback(slack_event.type):
        print("unknown event:", slack_event.type)
        return {"error": "not handled"}

    event_type = slack_event.event["type"]
    is_message = slack.is_event_message(event_type)
    is_mention = slack.is_event_mention(event_type)
    is_bot = slack.is_bot_message(slack_event.event)
    if (is_message or is_mention) and not is_bot:
        print("posting to the channel")
        res = slack.post_message("message received")
        if res is None:
            raise HTTPException(status_code=500, detail="Failed to send message")
        else:
            print("message has been succesfully posted")

    print("done")
    return {"status": "ok"}
