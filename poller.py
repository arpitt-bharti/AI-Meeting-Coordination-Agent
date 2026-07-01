from langgraph.types import interrupt, Command
import time
from langchain_core.messages import HumanMessage
from email_data.fetch_pending_approval_data import save_pending_approval,pending_exists
from services.gmail_service import fetch_new_mails, mark_email_as_read
from graph_builders import confirmation_graph_builder,fresh_email_graph_builder
from dotenv import load_dotenv

load_dotenv(override=True)

while True:
    confirmation_Graph = confirmation_graph_builder.build_confirmation_graph()
    fresh_email_graph = fresh_email_graph_builder.build_fresh_email_graph()
    fetched_emails = fetch_new_mails()
    for mail in fetched_emails: 
        
        mail_payload = mail['email_data'] 
        messageId = mail_payload['id'] 
        mail_threadId = mail_payload['threadId'] 
        mail_content = mail_payload.get('snippet', '') 
        
        if pending_exists(mail_threadId) :
            print(f'This mail with threadId {mail_threadId} is already pending for approval, so skipping...')
            continue
        
        headers = mail_payload['payload']['headers']
        sender_email = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown Sender")
        
        config = {'configurable' : {'thread_id' : f'mail_session{mail_threadId}'}}
        
        if mail['graph_type'] == 'confirmation': 
            print('invoking confirmation graph...') 
            try : 
                confirmation_Graph.invoke({ 
                    'reply_email' : mail_content, 
                    'conversationData' : dict(mail['db_record']) 
                },config)
            
                state = confirmation_Graph.get_state(config) 
                if state.next:
                    approval = input('Shall I create an event at the confirmed time slot?') 
                    confirmation_Graph.invoke(Command(resume=approval), config) 
                    mark_email_as_read(messageId)
                    print('Marked mail as read')
            except Exception as e :
                print(f'Exception occured ! - {e}')
                
        else: 
            print('invoking fresh email graph...') 
            try:
                fresh_email_graph.invoke({ 
                    'messages' : [HumanMessage(content=mail_content)], 
                    'thread_id' : mail_threadId,
                    'extracted_email_info' : {
                        'sender_email_address' : sender_email
                    }
                    }, config)  
                state = fresh_email_graph.get_state(config)
                
                if state.next:
                    save_pending_approval(
                        thread_id=mail_threadId,
                        graph_type="fresh_email",
                        recipient=state.values["extracted_email_info"]["sender_email_address"], 
                        agenda=state.values["extracted_email_info"]["agenda"],
                        draft_email=state.values["draft_response"]["body"]
                    )
                    print("Pending approval saved.")
    
            except Exception as e:
                print(f'Exception occured ! : {e}') 
    print() 
    time.sleep(20)
