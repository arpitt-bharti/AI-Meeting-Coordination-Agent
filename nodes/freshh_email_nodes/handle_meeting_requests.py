from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from states.fresh_graph_state import Fresh_Email_State, meetingDetails
from dotenv import load_dotenv

load_dotenv(override=True)

extract_llm = ChatOpenAI(model='gpt-5-nano')
extract_llm_with_SO = extract_llm.with_structured_output(meetingDetails)

def handle_meeting_requests(state : Fresh_Email_State) :
    PROMPT = f''' 
    You are an agent whose work is to extract important details from e-mails. 
    === DETERMINISTIC EMAIL METADATA ===
    Sender Info: {state["extracted_email_info"].get("sender_email_address", "Not Provided")}
    threadId : {state["thread_id"]}
     === EMAIL CONTENT BODY ===
    Here's the email - {state["messages"][-1].content}
    When you are provided with an e-mail,
    you have to extract things like :-
    - sender's name(if provided in email)
    - agenda - the agenda/motive for the meeting
    - requested day - the day they're proposing the meeting for
    - time-preference - their preferred/proposed time slot - The normalized target time extracted from the email in strict '%I:%M %p' format (e.g., '04:00 PM', '11:30 AM').
                        If vague like 'somewhere near to 11 AM', normalize it to the exact top of the hour like '11:00 AM'."
    - time_duration - the duration of the meeting
    If the email contains non-specific information such as  :-
    "Any time next week"
    "Sometime after the holiday" 
    "Whenever you're free"
    "June 25-27" 
    then make it as requires more clarification.
    '''

    response = extract_llm_with_SO.invoke(
        input=[SystemMessage(content=PROMPT)]
    )
    print(response)
    return {
        'extracted_email_info' : response
    }