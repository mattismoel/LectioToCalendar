import os, sys
import datetime
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from lectio import Lectio
  
class lectioToCalendar:
    def __init__(self, usr, psw, schl_id, cal_id):

        # Login using LectioScraper - [https://github.com/fredrikj31/LectioScraper]
        self.lec = Lectio(usr, psw, schl_id)
        
        # Load abbreviations/codes for activities
        if os.path.exists('abbreviations.json'):
            f = open('abbreviations.json')
            self.codes = json.load(f)
        else:
            raise Exception("File 'abbreviations.json' not found :(")
        
        
        # Define id of target calendar - use 'service.calendarList()' to see all id's
        self.calendarId = cal_id
        
        # Define scope, Google Calendar API
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        
        # Load Google Calendar API credentials/token
        self.creds = None

        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        if not self.creds or not self.creds.valid: #Login if no token is found
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)
        
    def lessonCodeToText(self, code):
        # Finds matching names for abbreviations/codes of activities
        new_name = code
        
        for i in self.codes:
            if i == code:
                new_name = self.codes[i]
        return new_name
        
    def getFormattedSchedule(self, week):
        # Gets Lectio schedule and formats to Google Calendar format
    
        lectio_scheme = self.lec.getSchedule(week)
        Schedule = []
        
        # Formatting all events in the given week
        for lectio_event in lectio_scheme:
            
            if lectio_event["Time"] == " ":
                continue
            
            if lectio_event["Title"] == " ":
                # Set title to generic if none are specified
                summary = self.lessonCodeToText(lectio_event["Team"])
            else:
                if lectio_event["Team"] != " ":
                    summary = lectio_event["Title"] + " - " + self.lessonCodeToText(lectio_event["Team"])
                else:
                    summary = lectio_event["Title"]
                
            if lectio_event["Status"] == "Aflyst!":
                color = "4" #for bold red (11)
                summary = "Aflyst! " + summary
                
            elif lectio_event["Status"] == "Ændret!":
                color = "2" #bold green (10)
            else:
                color = "1" #bold blue (9)
            
            location = None
            if lectio_event["Room"] != " ":
                location = "Lokale: " + lectio_event["Room"]
            
            description = ""
            if lectio_event["Teacher"] != " ":
                description = lectio_event["Teacher"]
            
            if lectio_event["Note"] != []:
                # Listing notes using basic html (only works in google calendar)
            
                note_txt = "<ul>"
                used_notes = []
                
                for note in lectio_event["Note"]:
                    if note[:2] == "- ":
                        # Bullet point found, adding and looking for sub-bullet points
                        note_txt += "<li>" + note[2:] + "</li>"
                        
                        search_for_quote = True
                        stop_search = False
                        
                        for i in lectio_event["Note"]:
                            if stop_search == True:
                                break
                                
                            if search_for_quote == True:
                                if i == note:
                                    search_for_quote = False
                            else:
                                # Continuing from parent bullet point
                                
                                if stop_search == True:
                                    continue
                                else:
                                    if i[:2] == "- ":
                                        # No sub-bullet points were found
                                        stop_search == True
                                    else:
                                        if i.lstrip()[:1] == "(" and i[-1:] == ")":
                                            # If only one sub-point
                                            note_txt += "<ul><li>" + i.lstrip()[1:][:-1] + "</li></ul>"
                                            stop_search == True
                                        else:
                                            if i.lstrip()[:1] == "(":
                                                # First sub-point
                                                note_txt += "<ul><li>" + i.lstrip()[1:] + "</li>"
                                                
                                            elif i[-1:] == ")":
                                                # Last sub-point
                                                note_txt += "<li>" + i.lstrip()[:-1] + "</li></ul>"
                                                stop_search == True
                                            
                                            else:
                                                # Middle sub-point
                                                note_txt += "<li>" + i.lstrip() + "</li>"
                                                
                                        used_notes.append(i)
                    else:
                        if note not in used_notes:
                            # Edge case notes
                            note_txt += "<li>" + note.replace("•", "").lstrip() + "</li>"
                            
                if lectio_event["Teacher"] != " ":
                    # Line break to make space between lines
                    description += "<br><br>"
                    
                description += "<b>Note/lektie:</b> " + note_txt.replace("[...]", "") + "</ul>"
            else:
                if lectio_event["Teacher"] != " ":
                    # Line break to make space between lines
                    description += "<br>"
            
            # Adding link to the original Lectio event
            description += '<a href="https://www.lectio.dk/lectio/143/aktivitet/aktivitetforside2.aspx?absid=' + lectio_event["Id"] + '">Læs mere</a>'
            
            # Formatting date and time to correct format - from "DD/MM-YYY HH:MM til HH:MM" to "YYYY-MM-DDTHH:MM:SS.MMMZ"
            times = lectio_event["Time"].split(" til ")
            date = times[0].split()[0].split("-")
            formatted_date = date[1] + "-" + date[0].split("/")[1] + "-" + date[0].split("/")[0]
            
            dateTime_start = formatted_date + 'T' + times[0].split()[1] + ':00+01:00'
            dateTime_end = formatted_date + 'T' + times[1] + ':00+01:00'
            
            # Building dict with all necessary information
            event = {
              'id': lectio_event["Id"],
              'summary': summary,
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
            if location != None:
                # If location is relevant, then add it
                event['location'] = location
            
            # Append to list of all events
            Schedule.append(event)
            
        return Schedule

    def updateCalendar(self, weekSchedule):

        # Calculating first datetime of week
        first_event_datetime = datetime.datetime.strptime(weekSchedule[0]["start"]["dateTime"][:-6], '%Y-%m-%dT%H:%M:%S')
        week_start_datetime = (first_event_datetime - datetime.timedelta(days=first_event_datetime.weekday())).replace(minute=0, hour=0, second=0)
        week_end_datetime = (week_start_datetime + datetime.timedelta(days=6)).replace(minute=59, hour=23, second=59)

        #print(week_start_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"))
        #print(week_end_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"))
        
        # Getting events from calendar
        events = self.service.events().list(calendarId=self.calendarId, timeMin=week_start_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"), timeMax=week_end_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00")).execute()
        
        old_events = []
        new_events = []
        
        for old_event in events['items']:
            old_events.append(old_event["id"])
            
        for new_event in weekSchedule:
            new_events.append(new_event["id"])
        
        extra_events = []
        missing_events = []
        
        # Looking for differences between Google Calendar and Lectio schedule
        if sorted(new_events) != sorted(old_events):
            extra_events = list(set(sorted(old_events)) - set(sorted(new_events)))
            missing_events = list(set(sorted(new_events)) - set(sorted(old_events)))

        #print("Extra events (to be deleted): " + str(extra_events))
        #print("Missing events (to be added): " + str(missing_events))
        
        for extra_event in extra_events:
            # Deleting extra events
            self.service.events().delete(calendarId=self.calendarId, eventId=extra_event).execute()
        
        for missing_event in missing_events:
            for event in weekSchedule:
                if event["id"] == missing_event:
                    # Inserting new events into specified Google Calendar
                    try:
                        self.service.events().insert(calendarId=self.calendarId, body=event).execute()
                        #print(str(missing_event) + " added to the calendar")
                        break
                    except HttpError:
                        # Updating missing events for specified Google Calendar
                        try:
                            self.service.events().update(calendarId=self.calendarId, eventId=missing_event, body=event).execute()
                            #print(str(missing_event) + " updated in the calendar")
                            break
                        except:
                            print("Missing event not inserted/updated: " + missing_event)
                            
        # Updating remaining events for specified Google Calendar
        for i in weekSchedule:
            if i["id"] not in extra_events and i["id"] not in missing_events:
                try:
                    # Updating existing event
                    self.service.events().update(calendarId=self.calendarId, eventId=i['id'], body=i).execute()
                except:
                    print("Existing event not updated: " + i["summary"])

        #print("Weekly schedule updated!")
            