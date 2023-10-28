# backend

## usage

- Slack トークンを ./backend/.slack.key に保存する
- OpenAI API Key を ./backend/.openai.key に保存する
- Poetry をインストール

```
poetry install 
poetry shell
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```