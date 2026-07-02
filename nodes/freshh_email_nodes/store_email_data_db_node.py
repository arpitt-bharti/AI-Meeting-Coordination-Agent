import json
from pathlib import Path
import sqlite3, os 
from datetime import datetime
from states.fresh_graph_state import Fresh_Email_State

folder_path = Path(r'C:\AppyProjects\CustomGenAIProjects\ai_meeting_coordination_agent\email_data')

def store_email_data_db_node(state : Fresh_Email_State) :
    proposed_slots = json.dumps(state['recommended_slots']) 
    conn = sqlite3.connect(folder_path/'email_data.db')
    cursor = conn.cursor()
    cursor.execute(
        (''' 
        INSERT INTO scheduling_conversations (
            threadId,    
            recipient_address, 
            proposed_slots,       
            status,         
            created_at,
            agenda              
        ) VALUES (?,?,?,?,?,?)
        '''
        ),
        (
            state['thread_id'], state['extracted_email_info']['sender_email_address'], proposed_slots,
            'Waiting_For_Reply', datetime.now().isoformat(), state['extracted_email_info']['agenda']
        )
    )
    conn.commit()
    #conn.close()
    print('Record saved successfully !')
    