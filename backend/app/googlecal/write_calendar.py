import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def add_event_to_calendar(event_data):
    # トークンの読み込みまたは新しいトークンの取得
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './app/googlecal/credentials.json', ['https://www.googleapis.com/auth/calendar'])
            creds = flow.run_local_server(port=8081)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    # Google Calendar APIクライアントのビルド
    service = build('calendar', 'v3', credentials=creds)

    # イベントのフォーマット
    event = {
        'summary': event_data['summary'],
        'location': event_data['location'],
        'description': f"参加者: {event_data['member']}",
        'start': {
            'dateTime': event_data['start'],
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': event_data['end'],
            'timeZone': 'Asia/Tokyo',
        },
    }

            #     "properties": {
            #     "summary": {
            #         "type":"string",
            #         "desctiprtion":"イベントのタイトル",
            #     },
            #     "location": {
            #         "type":"string",
            #         "description":"イベントの開催場所",
            #     },
            #     "member": {
            #         "type":"string",
            #         "description" : "イベントの参加者",
            #     },
            #     "start": {
            #         "type": "Date",
            #         "description":"開始時刻",
            #     },
            #     "end": {
            #         "type": "Date",
            #         "description":"終了時刻",
            #     },
            # },

    # イベントの追加
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"イベントが追加されました: {event['htmlLink']}")

# # イベントデータ
# event_data = {
#     "start_time": "2023-10-30T18:00:00+09:00",
#     "end_time": "2023-10-30T19:00:00+09:00",
#     "title": "MTG",
#     "place": "場所未設定",
#     "member": "未定"
# }

# add_event_to_calendar(event_data)
