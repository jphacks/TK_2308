import json


from . import chatgpt
from .googlecal.write_calendar import add_event_to_calendar

BOOKING_TOOKENS = ["調整", "ミーティング", "空いてる","空いている", "あいてる","あいている", "予定","面談","会議","日程","空き","あき","約束","スケジュール","都合","時間","カレンダー","打ち合わせ","日時"]


def is_asking_for_booking(message: str) -> bool:
    # メンションがついていればデフォルトで予定調整依頼として扱う
    return True

    # 予約後リストから半手しいたい場合は以下
    #for token in BOOKING_TOOKENS:
    #    if token in message:
    #        print(f"message contains '{token}'")
    #        return True
    #
    #return False


def create_booking(my_schedules: str, message: str):
    message_str = f"「相手のメッセージ：{message}」「自分のスケジュール：{my_schedules}」"

    res = chatgpt.send_chat(message_str)
    return res


def add_event_if_triggered(chat_response: dict):
    if not chatgpt.is_function_triggered(chat_response):
        return False

    # 関数を使用すると判断された場合

    message = chat_response["choices"][0]["message"]
    # 使うと判断された関数名
    function_name = message["function_call"]["name"]
    # その時の引数dict
    arguments = json.loads(message["function_call"]["arguments"])

    print(function_name)
    print(arguments)

    event = create_event(**arguments)

    add_event_to_calendar(event)

    return True


def create_event(
    summary,
    start,
    end,
    location=None,
    description=None,
    member=None,
    timeZone="Asia/Tokyo",
):
    event = {
        "summary": summary,
        "location": location,
        "description": None if member is None else f"参加者: {member}",
        "start": {
            "dateTime": start,
            "timeZone": timeZone,
        },
        "end": {
            "dateTime": end,
            "timeZone": timeZone,
        },
    }
    return event
