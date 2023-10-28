import openai

GPT_MODEL="gpt-4"

DEFAULT_SYSTEM_PROMPT= """
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

def send_chat(
    user_message: str,
    system_message: str = DEFAULT_SYSTEM_PROMPT
) -> openai.ChatCompletion:
    res = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            },
        ],
    )

    print("prompt:", system_message, user_message)
    print("Got response:", res)

    return res