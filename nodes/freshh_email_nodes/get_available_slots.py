from collections import defaultdict
from datetime import datetime, timedelta
from services.calendar_service import list_upcoming_events
from states.fresh_graph_state import Fresh_Email_State
from dotenv import load_dotenv

load_dotenv(override=True)

WORK_START_HOUR = 10
WORK_END_HOUR = 19
MEETING_DURATION = 30


def get_available_slots(state:Fresh_Email_State):
    print('inside get_available_slots ...')
    events = list_upcoming_events()
    events_by_day = defaultdict(list)
    for event in events:
        start = datetime.fromisoformat(event["start"]["dateTime"])
        end = datetime.fromisoformat(event["end"]["dateTime"])
        events_by_day[start.date()].append((start, end))
    
    available_slots = {}
    for day, busy_slots in events_by_day.items():
        busy_slots.sort(key=lambda x: x[0]) 
        tz = busy_slots[0][0].tzinfo
        
        work_start = datetime.combine(
            day,
            datetime.min.time()
        ).replace(
            hour=WORK_START_HOUR,
            tzinfo=tz
        )

        work_end = datetime.combine(
            day,
            datetime.min.time()
        ).replace(
            hour=WORK_END_HOUR,
            tzinfo=tz
        )

        cursor = work_start
        day_slots = []
        for event_start, event_end in busy_slots:
            while cursor + timedelta(minutes=MEETING_DURATION) <= event_start:
                day_slots.append(
                    (
                        cursor.strftime("%Y-%m-%d %H:%M"),
                        (cursor + timedelta(minutes=MEETING_DURATION)).strftime("%Y-%m-%d %H:%M")
                    )
                )
                cursor += timedelta(minutes=MEETING_DURATION)
            cursor = max(cursor, event_end)

        while cursor + timedelta(minutes=MEETING_DURATION) <= work_end:
            day_slots.append(
                (
                    cursor.strftime("%Y-%m-%d %H:%M"),
                    (cursor + timedelta(minutes=MEETING_DURATION)).strftime("%Y-%m-%d %H:%M")
                )
            )
            cursor += timedelta(minutes=MEETING_DURATION) 
        available_slots[str(day)] = day_slots
    
    print(state["extracted_email_info"]["time_preference"] ) 
    return {
        'available_slots' : available_slots 
    }  