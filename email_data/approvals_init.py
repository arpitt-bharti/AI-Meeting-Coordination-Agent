from pathlib import Path 
import sqlite3

path = Path(r'C:\AppyProjects\CustomGenAIProjects\ai_meeting_coordination_agent\email_data')

def create_pending_approval_table():
    approvals_db = path/'pending_approval_mails.db' 
    with sqlite3.connect(approvals_db) as conn: 
        cursor = conn.cursor() 
        
        cursor.execute(
            ''' 
            CREATE TABLE IF NOT EXISTS pending_approvals (
                threadId TEXT PRIMARY KEY,
                graph_type TEXT,
                recipient TEXT,
                agenda TEXT,
                draft_email TEXT
            );
            '''
        )
        print(f"Database ready! File located or created at: {approvals_db.resolve()}")
        
        
if __name__ == '__main__' :
    create_pending_approval_table()