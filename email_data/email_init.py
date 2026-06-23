from pathlib import Path
import sqlite3, os


def create_db(path) : 
    os.path.exists(path/'email_data.db')
    conn = sqlite3.connect(path/'email_data.db')
    cursor = conn.cursor()
        
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS scheduling_conversations(
            threadId                TEXT    PRIMARY KEY,
            recipient_address       TEXT,
            proposed_slots          TEXT, 
            status                  TEXT,
            created_at              DATETIME,
            agenda                  TEXT
        )
        '''
    )
    
    conn.commit()
    print("Database connection checked and ready!")
    
if __name__ == '__main__' :
    folder_path = Path(r'C:\AppyProjects\CustomGenAIProjects\ai_meeting_coordination_agent\email_data')
    create_db(folder_path)