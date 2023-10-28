from . import chatgpt


def create_booking(my_schedules: str, message: str):
    message_str = f"「相手のメッセージ：{message}」「自分のスケジュール：{my_schedules}」"

    res = chatgpt.send_chat(message_str)
    return res
