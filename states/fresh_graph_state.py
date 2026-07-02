
from typing import Annotated, TypedDict
from langgraph.graph import add_messages
from typing import Optional
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

#structured output for extraction
class meetingDetails(TypedDict):
    sender_name : Optional[str] = 'No Name Provided'
    sender_email_address : str
    agenda : str
    requested_day : list[str]
    time_preference : str
    time_duration : int
    
#Structured Output for draft email
class draft_email_SO(TypedDict) : 
    subject : str 
    body : str

#defining the state
class Fresh_Email_State(TypedDict):
    messages : Annotated[list, add_messages]
    intent : str 
    extracted_email_info : meetingDetails 
    needs_clarification : bool 
    available_slots : dict 
    draft_response : draft_email_SO 
    recommended_slots : list
    draft_email_approved : bool
    thread_id : str
    