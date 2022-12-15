creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())


#Find user calenders
'''
page_token = None
service = build('calendar', 'v3', credentials=creds)
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']:
    print(calendar_list_entry['summary'] + " - " + calendar_list_entry['id'])
  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break

'''

try:
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='f706b82bde3171dab3602e0fdf46d17c166c82feb0054048612abb6e7d057175@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

except HttpError as error:
    print('An error occurred: %s' % error)

