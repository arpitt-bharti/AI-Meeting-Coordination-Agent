from states.fresh_graph_state import Fresh_Email_State

def no_meeting_node(state : Fresh_Email_State) :
    print('inside no_meeting_node') 
    return { 
        'messages' : 'This is not a meeting request E-mail. So no action required from me.' 
    }