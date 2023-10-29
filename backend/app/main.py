from datetime import datetime

import openai
from .googlecal.googlecal import read_schedule_from_google
from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks

from . import schemas, slack, booking, summarize
from .lib import env

app = FastAPI()


with open(".openai.key", "r") as f:
    openai.api_key = f.read()


if env.is_prod():
    print("*** RUNNING ON PRODUCTION ENV ***")
else:
    print("--- Running on development env ---")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat", response_model=schemas.Chat)
def post_chat(chat: schemas.ChatPost):
    cal = read_schedule_from_google()
    schedules_str = ",".join(str(item) for item in cal)

    res = booking.create_booking(schedules_str, chat.message)
    content = res.choices[0].message.content

    res = chatgpt.send_chat(message_str)
    content = res.choices[0].message.content
    if content is None:
        return

    return schemas.Chat(message=chat.message, response=content)


@app.post("/search", response_model=schemas.SummarizeResult)
def post_search(sum: schemas.SummarizePost):
    from_date = datetime.fromisoformat(sum.from_date)
    to_date = datetime.fromisoformat(sum.to_date)

    messages = slack.search_messages(sum.channel_name, from_date, to_date)
    print(messages)

    res = summarize.summarize_messages(messages)
    summary = res.choices[0].message.content

    print(summary)

    slack.post_message(summary)

    return {"status": "ok"}


@app.post("/slack/events")
async def slack_events(
    request: Request, slack_event: schemas.SlackEvent, background_tasks: BackgroundTasks
):
    print("/slack/events")

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

    response = None

    event_type = slack_event.event["type"]
    is_message = slack.is_event_message(event_type)
    is_mention = slack.is_event_mention(event_type)
    is_bot = slack.is_bot_message(slack_event.event)

    if (is_message or is_mention) and not is_bot:
        print("handling normal message")
        response = handle_message(slack_event, background_tasks)
    else:
        raise HTTPException(status_code=400, detail="Unsupported event")

    print("done")

    return response


def handle_message(event: schemas.SlackEvent, background_tasks: BackgroundTasks):
    print("posting to the channel")

    message = str(event.event["text"])
    response_message = "message received"

    if summarize.is_asking_for_summary(message):
        print("is summary request")

        background_tasks.add_task(add_hatching_reaction, event)
        background_tasks.add_task(generate_summary, event)

        return {"status": "ok"}

    elif booking.is_asking_for_booking(message):
        print("is booking")

        background_tasks.add_task(add_eyes_reaction, event)
        background_tasks.add_task(create_booking, event)

        return {"status": "ok"}

    res = slack.post_message(response_message)
    if res is None:
        raise HTTPException(status_code=500, detail="Failed to send message")
    else:
        print("message has been succesfully posted")

    return {"status": "ok"}


def add_eyes_reaction(event: schemas.SlackEvent):
    name = "eyes"
    ts = event.event["ts"]
    channel_id = event.event["channel"]

    res = slack.add_reaction(name, ts, channel_id)

    if res is None:
        print("WARNING: failed to add a reaction")


def add_hatching_reaction(event: schemas.SlackEvent):
    name = "hatching_chick"
    ts = event.event["ts"]
    channel_id = event.event["channel"]

    res = slack.add_reaction(name, ts, channel_id)

    if res is None:
        print("WARNING: failed to add a reaction")


def create_booking(event: schemas.SlackEvent):
    print("creating booking. target event:", event)
    cal = read_schedule_from_google()
    schedules_str = ",".join(str(item) for item in cal)

    res = booking.create_booking(schedules_str, event.event["text"])
    content = res.choices[0].message.content

    res = slack.post_message(content)
    if res is None:
        print("Error: failed to post message")
    else:
        print("message has been succesfully posted")


def generate_summary(event: schemas.SlackEvent):
    print("generating summary. target event:", event)
    from_date = datetime.now()
    to_date = datetime.now()

    # 要約依頼メッセージを受け取ったチャンネルを要約してもらう場合は以下
    # channel_id = event.event["channel"]
    # channel_name = slack.get_channel_info(channel_id)["channel"]["name"]

    # 特定のチャンネルの要約を生成さえる
    channel_name = "time-tappun"

    user_prompt = event.event["text"]

    messages = slack.search_messages(channel_name, from_date, to_date)
    print("messages to summarize:", messages)

    res = summarize.summarize_messages(user_prompt, messages)
    summary = res.choices[0].message.content

    print("generated summary:", summary)

    slack.post_message(summary)
