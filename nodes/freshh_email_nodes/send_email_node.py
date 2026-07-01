from services.gmail_service import send_message
from states.fresh_graph_state import Fresh_Email_State
from dotenv import load_dotenv

load_dotenv(override=True)

def send_email_node(state : Fresh_Email_State) :
    recipient = state['extracted_email_info']['sender_email_address']
    subject = state['draft_response']['subject']
    body = state['draft_response']['body'] 
    print('Sending email now ...') 
    result = send_message(recipient, subject, body)
    print(result)
    return  {
        'thread_id' : result['threadId']
    }
    
    