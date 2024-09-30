import os
import base64
import json
import win32evtlog
import win32evtlogutil
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Set the SCOPES for Gmail API access
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    token_path = 'token.json'

    # Load credentials from the token.json file if exists
    if os.path.exists(token_path):
        with open(token_path, 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)

    # If no credentials or they're invalid, go through the OAuth2 flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future runs
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


# Function to send an email using Gmail API
def send_email(creds, to_email, subject, message_text):
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(message_text)
    message['to'] = to_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        message = (service.users().messages().send(userId='me', body={'raw': raw_message}).execute())
        print(f"Message sent successfully! Message ID: {message['id']}")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

# Function to check for critical or error events in the Windows Event Log
def check_event_logs():
    log_type = 'System'  # You can also use 'Application' or other logs
    server = 'localhost'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    handle = win32evtlog.OpenEventLog(server, log_type)
    events = win32evtlog.ReadEventLog(handle, flags, 0)

    critical_errors = []
    for event in events:
        event_id = event.EventID & 0xFFFF
        event_category = event.EventCategory
        event_type = event.EventType
        event_source = event.SourceName
        event_time = event.TimeGenerated.Format()
        event_msg = win32evtlogutil.SafeFormatMessage(event, log_type)

        if event_type == win32evtlog.EVENTLOG_ERROR_TYPE or event_type == win32evtlog.EVENTLOG_WARNING_TYPE:
            critical_errors.append({
                'time': event_time,
                'source': event_source,
                'event_id': event_id,
                'category': event_category,
                'message': event_msg
            })

    return critical_errors

# Main function
def main():
    critical_errors = check_event_logs()

    if critical_errors:
        creds = authenticate_gmail()
        to_email = 'your_email'
        subject = 'Critical Event Log Detected'
        message_text = "The following critical or error events were detected in the Event Log:\n\n"

        for error in critical_errors:
            message_text += f"Time: {error['time']}\n"
            message_text += f"Source: {error['source']}\n"
            message_text += f"Event ID: {error['event_id']}\n"
            message_text += f"Category: {error['category']}\n"
            message_text += f"Message: {error['message']}\n"
            message_text += "-"*40 + "\n"

        send_email(creds, to_email, subject, message_text)
    else:
        print("No critical or error events found.")

if __name__ == '__main__':
    main()
