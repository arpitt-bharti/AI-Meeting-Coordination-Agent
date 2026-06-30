from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from states.fresh_graph_state import Fresh_Email_State
from typing import Literal, TypedDict
from dotenv import load_dotenv

load_dotenv(override=True)

#Structured output for general agent 
class Intent(TypedDict) : 
    intent : Literal['Meeting_Email', 'Not_Meeting_Email']

#classifier LLM
load_dotenv(override=True)
classify_llm = ChatOpenAI(model='gpt-5')
classify_llm_with_so = classify_llm.with_structured_output(Intent)

def classify_email_agent(state : Fresh_Email_State) :
    print('inside classify email agent ...')
    SYSTEM_PROMPT = f"""You are an expert triage agent classifying email intent.

    [CRITICAL INSTRUCTIONS]
    Categorize the incoming email into exactly one of these two intents:
    - 'Meeting_Email': Select this if the sender is asking, proposing, or suggesting a meeting, interview, sync, phone call, calendar slot, or scheduling an explicit block of time (even if phrased casually like "available for a meeting on...", "free tomorrow?", or "let's connect").
    - 'Not_Meeting_Email': Select this if the email is about anything else (e.g., support tickets, updates, general info, spam, newsletters).

    Analyze carefully: A casual invitation like "available on 26th June around 11 PM?" IS A MEETING EMAIL.
    Here's the email - \n {state['messages']}
    """
    
    response = classify_llm_with_so.invoke(
        input=[SystemMessage(content=SYSTEM_PROMPT)] 
    )
    print(response)
    return {
        'intent' : response['intent']
    }
    
    
def post_classication_routing(state : Fresh_Email_State) :
    print('inside classification routing...')
    print(state['intent']) 
    return 'handle_meeting_requests' if state['intent']=='Meeting_Email' else 'Not_Meeting_Email'