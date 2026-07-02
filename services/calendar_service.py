import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# 1. Define your scopes (permissions)
# If modifying events, use: 'https://googleapis.com'
#SCOPES = ['https://googleapis.com.readonly']
SCOPES = [
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/gmail.readonly', 
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.modify'
        ]

def get_calendar_service():
    creds = None
    print('inside get_calendar_service')
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
    return build('calendar', 'v3', credentials=creds)

def list_upcoming_events():
    try:
        service = get_calendar_service()        
        print("\nFetching the next 10 events from your primary calendar...\n")
        events_result = service.events().list(
            calendarId='primary', 
            maxResults=10, 
            singleEvents=True, 
            orderBy='startTime'
        ).execute()
        #print(f'event results - {events_result}') 
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.') 
            return

    except HttpError as error:
        print(f'An API error occurred: {error}') 
        
    return events

def create_event(summary, location, starttime_raw, endtime_raw, attendees): 
    print('Creating event .....')
    service = get_calendar_service()
    start_dt = datetime.strptime(starttime_raw.strip(), "%Y-%m-%d %H:%M") 
    end_dt = datetime.strptime(endtime_raw.strip(), "%Y-%m-%d %H:%M")

    starttime_iso = start_dt.isoformat() + "+05:30"  #2026-06-20T17:00:00+05:30
    endtime_iso = end_dt.isoformat() + "+05:30"
    payload = {
        'summary' : summary,
        'location' : location,
        'start' : {
            'dateTime': starttime_iso,     
            'timeZone': 'Asia/Kolkata' 
        },
        'end': { 
            'dateTime': endtime_iso,     
            'timeZone': 'Asia/Kolkata'
        },
        'attendees' : attendees
    }
    
    event = service.events().insert(
            calendarId='primary',
            body=payload).execute()
    
    print ('Event created: %s' % (event.get('htmlLink'))) 
    
    
if __name__ == '__main__':
    events = list_upcoming_events()
