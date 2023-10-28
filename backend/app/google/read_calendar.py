import datetime
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

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
            'credentials.json', ['https://www.googleapis.com/auth/calendar.readonly'])
        creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

# Google Calendar APIクライアントのビルド
service = build('calendar', 'v3', credentials=creds)


# 現在から1年後までのイベントを取得
now = datetime.datetime.utcnow().isoformat() + 'Z'  # 現在のUTC時刻
end_time = (datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat() + 'Z'  # 現在から1年後のUTC時刻

events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=end_time, 
                                      singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])

for event in events:
    start_time = event['start'].get('dateTime', event['start'].get('date'))
    end_time = event['end'].get('dateTime', event['end'].get('date'))
    location = event.get('location', "場所未設定")  # locationが設定されていない場合は"場所未設定"と表示
    title = event.get('summary', "タイトル未設定")  # summaryが設定されていない場合は"タイトル未設定"と表示

    print(f"開始時刻: {start_time}, 終了時刻: {end_time}, 場所: {location}, タイトル: {title}")