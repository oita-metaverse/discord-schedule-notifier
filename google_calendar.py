import datetime
import googleapiclient.discovery
import google.auth

def get_calendar():
    # 認証スコープと認証情報の設定
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    CLIENT_SECRET_FILE = 'client_secret.json'  # OAuth 2.0 クライアント ID の JSON ファイル

    # Google Calendar API と接続
    gapi_creds = google.auth.load_credentials_from_file(CLIENT_SECRET_FILE, SCOPES)[0]
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
    
    return service