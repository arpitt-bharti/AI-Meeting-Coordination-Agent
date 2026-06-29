from pathlib import Path
import sqlite3

DB_PATH = Path(r'C:\AppyProjects\CustomGenAIProjects\ai_meeting_coordination_agent\email_data\pending_approval_mails.db')

def save_pending_approval(thread_id,graph_type,recipient,agenda,draft_email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO pending_approvals
        (threadId, graph_type, recipient, agenda, draft_email)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            thread_id,
            graph_type,
            recipient,
            agenda,
            draft_email
        )
    )

    conn.commit()
    conn.close()


def get_pending_approvals():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pending_approvals"
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def delete_pending_approval(thread_id):
    print(f'inside delete_pending_approval for deleting thread I - {thread_id}')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM pending_approvals
        WHERE threadId = ?
        """,
        (thread_id,)
    )
    conn.commit()
    print('Deleted this email entry from pending_approvals table...')

def pending_exists(thread_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        ''' 
        SELECT 1
        FROM pending_approvals
        WHERE threadId = ?
        ''', (thread_id,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    return result is not None