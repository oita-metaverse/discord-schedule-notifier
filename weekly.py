from datetime import datetime, timedelta
from google_calendar import get_calendar
from dotenv import load_dotenv
load_dotenv()
import os

# 日時の設定
today = datetime.now().date()+ timedelta(days=1)
time_start = today.isoformat() + 'T00:00:00Z'
one_week_later = today + timedelta(days=6)
time_end = one_week_later.isoformat() + 'T23:59:59Z'

calendar_id = os.getenv('CALENDAR_ID')
service = get_calendar()

event_list = service.events().list(
     calendarId=calendar_id,
     timeMin=time_start,
     timeMax=time_end,
     maxResults=3, singleEvents=True,
     orderBy='startTime').execute()

content = "## 📅今週の予定\n"

# イベントを日付ごとにグループ化
events_by_date = {}
for event in event_list["items"]:
    start_time = event["start"]["dateTime"]
    event_date = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z").date()
    events_by_date.setdefault(event_date, []).append(event)

weekday_names = ["月", "火", "水", "木", "金", "土", "日"]

# グループ化されたイベントを日付順に表示
for event_date, events in sorted(events_by_date.items()):
    weekday = weekday_names[event_date.weekday()]
    formatted_date = event_date.strftime("%m/%d") + f"({weekday})"
    content += f"### {formatted_date}\n"

    for event in events:
        start_time = datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S%z").time()
        end_time = datetime.strptime(event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S%z").time()
        event_name = event["summary"]
        formatted_start_time = start_time.strftime("%H:%M")
        formatted_end_time = end_time.strftime("%H:%M")
        content += f"- {formatted_start_time} - {formatted_end_time}　{event_name}\n"

content = content[:-1]

# Discordに投稿
from discord_post import post
post(
     os.getenv('DISCORD_TOKEN'), 
     os.getenv('DISCORD_CHANNEL_ID'), 
     content
)