from . import chatgpt


BOOKING_TOOKENS = ["調整", "ミーティング", "空いてる", "あいてる", "予定"]


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
