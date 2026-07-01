from langgraph.types import interrupt, Command
from states.fresh_graph_state import Fresh_Email_State
from dotenv import load_dotenv

load_dotenv(override=True)

def hITL_node(state: Fresh_Email_State) :
    '''implements HITL'''
    print('inside HITL Node')
    
    human_response = interrupt("Waiting for human approval") 
    if human_response["approved"]: 
        updated_draft = state["draft_response"].copy()
        updated_draft['body'] = human_response["edited_email"] 
        return { 
        "draft_email_approved": True,
        "draft_response": updated_draft
    } 
    return {
        "draft_email_approved": False
    }
    

def approval_node_routing(state: Fresh_Email_State) :
    return 'send_email_action' if state['draft_email_approved'] else 'email_not_approved_action'