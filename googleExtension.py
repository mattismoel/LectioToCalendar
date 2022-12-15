import os, sys
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.lectio import Lectio
lec = Lectio()

SCOPES = ['https://www.googleapis.com/auth/calendar']
calendarId='7bdf11c5c1ac6f4032c851e580b7df97365f8305fe43e56968812b3fb454a86b@group.calendar.google.com'

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

def fetchWeekSchedule(week):
    lectio_scheme = lec.getSchedule(week)
    Schedule = []
    
    for lectio_event in lectio_scheme:
        
        if lectio_event["Time"] == " ":
            continue
        
        if lectio_event["Title"] == " ":
            summary = lectio_event["Team"]
        else:
            summary = lectio_event["Title"]
            
        if lectio_event["Status"] == "Aflyst!":
            color = "4" #red (11)
            summary = "Aflyst! " + summary
            
        elif lectio_event["Status"] == "Ændret!":
            color = "2" #green (10)
        else:
            color = "1" #blue (9)
            
        if lectio_event["Room"] != " ":
            location = "Lokale: " + lectio_event["Room"]
        else:
            location = lectio_event["Room"]
            
        description = lectio_event["Teacher"]
        
        if lectio_event["Note"] != []:
            note_txt = "<ul>"
            for note in lectio_event["Note"]:
                note_txt = note_txt + "<li>" + note[2:] + "</li>"
                
            description = description + "<br><br><b>Note/lektie:</b> " + note_txt.replace("[...]", "") + "</ul>"
        else:
            description += "<br>"
            
        description = description + '<a href="https://www.lectio.dk/lectio/143/aktivitet/aktivitetforside2.aspx?absid=' + lectio_event["Id"] + '">Lectio event</a>'
        
        times = lectio_event["Time"].split(" til ")
        date = times[0].split()[0].split("-")
        formatted_date = date[1] + "-" + date[0].split("/")[1] + "-" + date[0].split("/")[0]
        
        dateTime_start = formatted_date + 'T' + times[0].split()[1] + ':00+01:00'
        dateTime_end = formatted_date + 'T' + times[1] + ':00+01:00'
        
        #print(dateTime_start)
        #print(dateTime_end)
        
        event = {
          'id': lectio_event["Id"],
          'summary': summary,
          'location': location,
          'description': description,
          'locked': 'true',
          'colorId': color,
          'source.title': "Lectio event",
          'source.url': 'https://www.lectio.dk/lectio/143/aktivitet/aktivitetforside2.aspx?absid=' + lectio_event["Id"],
          'start': {
            'dateTime': dateTime_start,
            'timeZone': 'Europe/Copenhagen',
          },
          'end': {
            'dateTime': dateTime_end,
            'timeZone': 'Europe/Copenhagen',
          }
        }
        
        Schedule.append(event)
        
    return Schedule

def updateGoogleCalendar(week):
    print("Fetching events (" + week + ")...")

    weekSchedule = fetchWeekSchedule(week)
    service = build('calendar', 'v3', credentials=creds)

    for i in weekSchedule:
        try:
            service.events().insert(calendarId=calendarId, body=i).execute()
        except HttpError:
            try:
                service.events().update(calendarId=calendarId, eventId=i['id'], body=i).execute()
            except:
                print("Event not inserted/updated: " + i["summary"])
                
    print("Weekly schedule updated!")
    
updateGoogleCalendar("512022")