from langchain_core.messages import SystemMessage
from states.fresh_graph_state import Fresh_Email_State,draft_email_SO
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_openai import ChatOpenAI 
draft_email_llm = ChatOpenAI(model='gpt-5-nano') 
draft_email_llm_with_SO = draft_email_llm.with_structured_output(draft_email_SO)

def draft_reply(state : Fresh_Email_State) :
    print('inside draft_reply ...')
    PROMPT = f''' 
    You are working as a a personal e-mail drafting assistant for me. You are provided with a proposed meeting details
    and also, my available time slots. You have to draft a reply to the proposer, informing about the time slots which
    I will be available on, respond with the available time slots which are near the proposed meeting time. Respond with a maximum of 
    3-5 slots. 
    here arw the meetiong details : \n
    {state['extracted_email_info']} \n
    and here are my available slots \n
    {state['recommended_slots']}
    '''
    response = draft_email_llm_with_SO.invoke(
        input=[SystemMessage(content=PROMPT)]
    )
    print(response)
    return {
        'draft_response' : response
    }
    