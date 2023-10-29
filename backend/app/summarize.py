from . import chatgpt, slack


SUMMARIZE_TOOKENS = ["要約して"]


def summarize_messages(messages: list[slack.Message]):
    input = format_messages(messages)
    res = chatgpt.send_chat(input, system_message=chatgpt.SUMMARIZE_SYSTEM_PROMPT)
    res
    return res


def format_messages(messages: list[slack.Message]):
    format = """- 発言者: {}
    - 内容: {}"""

    formatted_messages = [format.format(msg.user, msg.text) for msg in messages]

    return "\n------\n".join(formatted_messages)


def is_asking_for_summary(message: str) -> bool:
    for token in SUMMARIZE_TOOKENS:
        if token in message:
            print(f"message contains '{token}'")
            return True

    return False
