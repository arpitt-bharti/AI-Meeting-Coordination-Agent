from pathlib import Path
import sqlite3

from states.confirmation_state import ConfirmationState

def update_email_data_in_db(replyState : ConfirmationState) :
    folder_path = Path(r'C:\AppyProjects\CustomGenAIProjects\ai_meeting_coordination_agent\email_data')

    print('inside update_email_data_in_db.... ')
    conn = sqlite3.connect(folder_path/'email_data.db') 
    cursor = conn.cursor() 
    print(replyState)
    cursor.execute(
        ''' 
        UPDATE scheduling_conversations
        SET status = ?
        WHERE threadId = ?
        ''' , ('Event Created', replyState['conversationData']['threadId']) 
    )
    conn.commit()
    print('\n Status has been updated !')
    