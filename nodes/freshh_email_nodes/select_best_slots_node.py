from datetime import datetime
from states.fresh_graph_state import Fresh_Email_State
from dotenv import load_dotenv

load_dotenv(override=True)

def select_best_slots(available_slots, date, preferred_time):
    print('inside select_best_slots ...')
    slots = available_slots.get(date, [])
    target_time = datetime.strptime(
        preferred_time,
        "%I:%M %p"
    )
    ranked = []
    for start, end in slots:
        start_dt = datetime.strptime( 
            start,
            "%Y-%m-%d %H:%M" 
        )
        diff = abs(
            (start_dt.hour * 60 + start_dt.minute)
            - (target_time.hour * 60 + target_time.minute) 
        )
        ranked.append((diff, start, end))
    ranked.sort(key=lambda x: x[0])
    return ranked[:3]


def select_best_slots_node(state: Fresh_Email_State):
       
    recommended_slots = select_best_slots(
        available_slots=state["available_slots"],
        date="2026-07-04",      # temporarily hardcoded 
        preferred_time=state["extracted_email_info"]["time_preference"] 
    )
    print(f'recommended slots - {recommended_slots}')
    return {
        "recommended_slots": recommended_slots
    } 