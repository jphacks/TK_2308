import openai

GPT_MODEL="gpt-3.5-turbo"
DEFAULT_SYSTEM_PROMPT= "日本語で返答してください。"

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

    print("Got response:", res)

    return res