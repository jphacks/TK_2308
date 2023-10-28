import openai
import json
from .googlecal.write_calendar import add_event_to_calendar

GPT_MODEL = "gpt-4"

DEFAULT_SYSTEM_PROMPT = """
あなたには，私の秘書として予定の管理業務に当たってもらいます．
メッセージとして，取引先の方から，MTGの日程調整等の連絡が来ますので，それに対して，別途与えた私のスケジュールをもとに，相手の要望の条件に沿ったスケジュール候補を可能な限り多く選択し，教えてください．
以下の点に注意してレスポンスを行なってください．
1. 予定調整の分数の単位は，相手からの要望がない限り30分刻みとする.
2. 返信テキストメッセージは，相手の口調に合わせ，私の代わりに丁寧な文章を生成すること．ChatGPTとしてのコメントは必要ない．
3. カレンダー上の情報から取得したテキストをもとに，そこに予定を入れることが可能かを考えること．例えば，北海道で予定が終わった後，沖縄の予定には参加できない．
4. あなたは鳥の秘書キャラクターなので，語尾に「ッピ！」「だッピ！」「ピィ〜！」などをつけてください．
5. 時間の長さの指定がない場合は，1時間単位で出力してください．
6. 提案の個数の指定がない場合は，

「相手のメッセージ：メッセージ内容」
「私のスケジュール：Date型のリスト」
といった形で与えられますので，適切な挨拶やお礼，スケジュールと相手のメッセージに基づいた予定の提示を行なってください．

日程の出力の方法は，以下の例に倣って出力してください．
11/1(月) 10:00~11:00, 13:00~14:00, 16:00~17:00
11/2(火) 10:00~11:00, 15:00~16:00

"""

my_functions = [
    {
        "name": "add_event_to_calendar",
        "description": "予定への参加が可能となった場合に呼ばれるfunction.予定の開始時間と終了時間，タイトル(やること)が決まっていたら，Googleカレンダーに追加する関数．面談やMTGなどのアポイントを求められ，そのタイミングに自身のスケジュールが空いていたら，関数を呼ぶ",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "ミーティングなどのアポイント予定を確保した際，保存するためのイベントのタイトル",
                },
                "location": {
                    "type": "string",
                    "description": "ミーティングなどのアポイント予定を確保した際，開催するための場所",
                },
                "member": {
                    "type": "string",
                    "description": "ミーティングなどのアポイント予定を確保した際，イベントの参加者. カンマ区切りで複数人登録可能",
                },
                "start": {
                    "type": "string",
                    "description": "ミーティングなどのアポイント予定を確保した際, 予定の開始時刻．dateTimeの形式であり，timezoneはAsia/Tokyo",
                    "format": "date-time",
                },
                "end": {
                    "type": "string",
                    "description": "ミーティングなどのアポイント予定を確保した際, 予定の終了時刻．dateTimeの形式であり，timezoneはAsia/Tokyo. 開始時刻のみの指定だった場合，1時間として確保",
                    "format": "date-time",
                },
            },
            "required": ["summary", "start", "end"],
        },
    }
]


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


def send_chat(
    user_message: str, system_message: str = DEFAULT_SYSTEM_PROMPT
) -> openai.ChatCompletion:
    res = openai.ChatCompletion.create(
        model=GPT_MODEL,
        functions=my_functions,
        function_call="auto",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    print("prompt:", system_message, user_message)
    print("Got response:", res)

    if is_function_triggered(res):
        # 関数を使用すると判断された場合

        # 使うと判断された関数名
        function_name = message["function_call"]["name"]
        # その時の引数dict
        arguments = json.loads(message["function_call"]["arguments"])

        print(function_name)
        print(arguments)

        event = create_event(**arguments)

        add_event_to_calendar(event)

    return res


def is_function_triggered(chat_response: dict):
    message = chat_response["choices"][0]["message"]
    return message.get("function_call") is not None
