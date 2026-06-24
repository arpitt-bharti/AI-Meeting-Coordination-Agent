import base64
from email.mime.text import MIMEText
import os.path
from pathlib import Path
import sqlite3
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 1. Define your scopes (permissions)
# If modifying events, use: 'https://googleapis.com'
#SCOPES = ['https://googleapis.com.readonly']
SCOPES = [
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/gmail.readonly', 
            'https://www.googleapis.com/auth/gmail.send'
        ]

def get_gmail_service():
    creds = None
    print('inside get_gmail_service')
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the user authorizes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES) 
    
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        print('no creds found or invalid creds...checking more')
        if creds and creds.expired and creds.refresh_token:
            print("Access token expired. Refreshing automatically using the Refresh Token...") 
            creds.refresh(Request())
        else:
            print("No tokens found. Initiating local browser login flow...")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run so the user doesn't have to re-login
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build and return the Calendar API Service client engine
    return build('gmail', 'v1', credentials=creds)


def send_message(to, subject, message_text):
    """Creates and sends an email message."""
    try:
        service = get_gmail_service()
        if service:
            print('Authenticated !')
        # 1. Create a standard MIME email structure
        message = MIMEText(message_text)
        message['to'] = to
        message['subject'] = subject

        # 2. Encode the entire email string into URL-safe Base64 format
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        create_message = {'raw': raw_message}

        # 3. Call the Gmail API messages.send method
        # 'me' represents the authenticated user account
        send_request = service.users().messages().send(userId='me', body=create_message)
        sent_details = send_request.execute()
        
        print(f"Success! Message sent successfully. Message ID: {sent_details['id']}")
        return sent_details

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    
    
def check_inbox() :
    print('Inside check_inbox...')
    service = get_gmail_service()
    
    # Query string: Only unread emails in the inbox
    search_query = "is:unread category:primary" 

    list_response = service.users().messages().list(
        userId='me', 
        q=search_query
    ).execute()

    messages = list_response.get('messages', [])
    return service, messages


def fetch_new_mails() :
    print('Inside fetch_new_mails...')
    db_file = Path(r'C:\AppyProjects\CustomGenAIProjects\ai_meeting_coordination_agent\email_data\email_data.db')
    processed_actions = [] 
    service, new_mails = check_inbox()
    with sqlite3.connect(db_file) as conn: 
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor() 
        
        for mail in new_mails:
            threadId = mail['threadId']
            messageId = mail['id'] 
            cursor.execute(
                ''' 
                SELECT * from scheduling_conversations WHERE threadId = ?
                ''' , (threadId,)
            )
            
            full_email = service.users().messages().get(userId='me', id=messageId).execute() 
            existing_convo = cursor.fetchone() 
        
            if existing_convo is not None:
                print('This email is a part of email chain....\n')
                processed_actions.append({
                    'graph_type':'confirmation',
                    'email_data':full_email,
                    'db_record':existing_convo
                })
            else:
                print('A fresh email')
                processed_actions.append({
                    'graph_type':'fresh',
                    'email_data':full_email,
                    'db_record':None
                })  
    return processed_actions


if __name__ == '__main__':
   
    # Execute the email configuration
    send_message(
        to="arpit.bharti503@gmail.com",
        subject="Automated Gmail API Test",
        message_text="Hellooo brooooo! This message was safely delivered using the official Gmail REST API."
    )