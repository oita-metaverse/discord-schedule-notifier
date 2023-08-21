from datetime import datetime
from google_calendar import get_calendar
from dotenv import load_dotenv
load_dotenv()
import os

# 日時の設定
today = datetime.now().date()
time_start = today.isoformat() + 'T00:00:00Z'
time_end = today.isoformat() + 'T23:59:59Z'

calendar_id = os.getenv('CALENDAR_ID')
service = get_calendar()

event_list = service.events().list(
     calendarId=calendar_id,
     timeMin=time_start,
     timeMax=time_end,
     maxResults=3, singleEvents=True,
     orderBy='startTime').execute()

if len(event_list["items"]) == 0:
    print("items is 0")
    exit()
    
content = "## 🔔本日の予定\n"

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