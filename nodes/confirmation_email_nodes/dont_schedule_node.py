from states.confirmation_state import ConfirmationState

def dont_schedule_node(replyState : ConfirmationState) :
    return{
        'schedule_meeting' : False
    }