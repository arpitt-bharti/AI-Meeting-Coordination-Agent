from typing import Literal, Optional, TypedDict

#slot SO
class SelectedSlot(TypedDict):
    slot_id: int
    start_time: str
    end_time: str
    
#structured output for reply email data extration
class ReplyExtraction(TypedDict) : 
    selected_slot : Optional[SelectedSlot] 
    explanation : Optional[str] 
    intent : Literal['Accepted_slot', 'Rejected_slot', 'Request Reschedule','Needs Clarification']

class ConfirmationState(TypedDict) :
    reply_email : str 
    replyEmailExtractedDetails : ReplyExtraction 
    conversationData:str 
    schedule_meeting : bool
    
