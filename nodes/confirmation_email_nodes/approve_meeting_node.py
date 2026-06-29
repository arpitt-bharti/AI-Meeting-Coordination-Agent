from states.confirmation_state import ConfirmationState
from langgraph.types import interrupt
from dotenv import load_dotenv

load_dotenv(override=True)

def approve_meeting_node(replyState:ConfirmationState) :   
    print('inside approve_meeting_node') 
    approve_meeting = f''' 
        {replyState['conversationData']['recipient_address']} has proposed a meeting for {replyState['conversationData']['agenda']} 
        We had given them these available slots - \n {replyState['conversationData']["proposed_slots"]} and he/she has chosen \n
        {replyState['replyEmailExtractedDetails']['selected_slot']} 
        Are you okay with me to schedule a meeting at the confirmed time? Pausing state for input !
        '''
    print(approve_meeting) 

    create_event = interrupt('Schedule Meeting ?  Yes/No...') 
    if create_event.lower() == 'yes': 
        return { 'schedule_meeting' : "Go_ahead" } 
    else:
        return { 'schedule_meeting' : "dont_schedule" }
    
    
def schedule_routing(replyState : ConfirmationState) : 
    return "create_event" if replyState["schedule_meeting"]=='Go_ahead' else 'dont_schedule' 