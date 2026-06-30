from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from states.confirmation_state import ConfirmationState,ReplyExtraction
from dotenv import load_dotenv

load_dotenv(override=True)

reply_extraction_llm = ChatOpenAI(model='gpt-5-nano') 
reply_extraction_llm_with_so = reply_extraction_llm.with_structured_output(ReplyExtraction)

def extractReplyEmailData (replyState : ConfirmationState) : 
    print('inside extractReplyEmailData...')
    SYSTEM= f''' You are provided an email and you have to extract important information from it so that the ceo can know 
    what is the other party's response to the original email was. 
    This is the received email - {replyState['reply_email']} 
    These were the proposed slots:
    {replyState['conversationData']['proposed_slots']}

    If the user accepts one of the proposed slots,
    return the EXACT slot from the list.
    ''' 
    response = reply_extraction_llm_with_so.invoke( 
        input=[SystemMessage(content=SYSTEM)] 
    ) 
    print(response) 
    return {
        'replyEmailExtractedDetails' : response 
    }