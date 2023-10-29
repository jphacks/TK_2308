# backend

## usage

- Bot をチャンネルに招待
- Slack トークンを ./backend/.slack.key に保存する
- Slack signing secret を ./backend/.slack-sign.key に保存する
- OpenAI API Key を ./backend/.openai.key に保存する
- Poetry をインストール
- Ngrok に登録
- Slack App の collabolator として登録

```
poetry install
poetry shell
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

新しいタブ

```
ngrok http 8080
```

- 表示された URL をコピる  
  - https://e35c-192-51-222-128.ngrok.io こんなやつ
- アプリの Event Subscriptions 設定から Request URL を &lt;URL&gt;/slack/events にする
  - 例: https://e35c-192-51-222-128.ngrok.io/slack/events
