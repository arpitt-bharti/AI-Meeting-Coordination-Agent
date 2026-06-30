from services.calendar_service import create_event 
from states.confirmation_state import ConfirmationState
from dotenv import load_dotenv

load_dotenv(override=True)

def create_event_node(replyState : ConfirmationState) : 
    print('inside create_event_node...')
    summary = replyState['conversationData']['agenda'] 
    location = 'Google Meet' 
    attendees = replyState['conversationData']['recipient_address'] 
    #selected_slot = "2026-06-20 17:00-17:30"
    start_time = replyState['replyEmailExtractedDetails']['selected_slot']['start_time'] 
    end_time = replyState['replyEmailExtractedDetails']['selected_slot']['end_time'] 
    print(start_time) 
    print(f'end time - {end_time}')
    create_event(summary, location,start_time, end_time,attendees)
    
    