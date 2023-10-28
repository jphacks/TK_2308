from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from slack_sdk.errors import SlackApiError

DEFAULT_CHANNEL = "#_gtb_bot"

with open("./.slack.key", "r") as f:
    TOKEN = f.read()

with open("/code/.slack-sign.key", "r") as f:
    SLACK_SIGNING_SECRET = f.read()

client = WebClient(token=TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)


def post_message(message: str, channel_name: str = DEFAULT_CHANNEL):
    try:
        response = client.chat_postMessage(channel=channel_name, text=message)
        print("got response:", response)
        return response
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")
        return None


def verify_signature(body: str, headers: dict):
    ok = signature_verifier.is_valid_request(body, headers)
    return ok


def is_verification(request_type: str) -> bool:
    return request_type == "url_verification"


def is_callback(request_type: str) -> bool:
    return request_type == "event_callback"


def is_event_message(event_type: str) -> bool:
    return event_type == "message"


def is_event_mention(event_type: str) -> bool:
    return event_type == "app_mention"


def is_bot_message(event: dict) -> bool:
    return "bot_id" in event
