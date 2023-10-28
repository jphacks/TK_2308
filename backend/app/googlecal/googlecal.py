import datetime
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def read_schedule_from_google():
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
                './app/googlecal/credentials.json', ['https://www.googleapis.com/auth/calendar.readonly'])
            creds = flow.run_local_server(port=8081)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                

    # Google Calendar APIクライアントのビルド
    service = build('calendar', 'v3', credentials=creds)

    # 現在から1週間のイベントを取得
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return events