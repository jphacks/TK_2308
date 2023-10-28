# backend

## usage

- Bot をチャンネルに招待
- Slack トークンを ./backend/.slack.key に保存する
- Slack signing secret を ./backend/.slack-sign.key に保存する
- OpenAI API Key を ./backend/.openai.key に保存する
- Poetry をインストール

```
poetry install 
poetry shell
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```