import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

DEFAULT_CHANNEL = "#_gtb_bot"

with open("./.slack.key", "r") as f:
    TOKEN = f.read()

client = WebClient(token=TOKEN)


def post_message(message: str, channel_name: str = DEFAULT_CHANNEL):
    try:
        response = client.chat_postMessage(channel=channel_name, text=message)
        print("got response:", response)
        return response
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")
        return None
