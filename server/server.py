import sys, os
import threading
from time import sleep
from datetime import datetime, timedelta 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calendar import lectioToCalendar

sync_weeks_ahead = 4 # Will update schedule x weeks ahead of today
current_week_sync_interval = 5.0 # Minutes between updating calendar for this week
future_week_sync_interval = 15.0 # Minutes between updating calendar future weeks

# Lectio login credentials
user_name = ""
password = ""
school_id = "" # In the URL when you visit Lectio

# Which Google calendar to use
calendar_id = 'primary'


def updateCurrentWeek():    

    ltc = lectioToCalendar(user_name, password, school_id, calendar_id)

    while True:
        today_date = datetime.today().isocalendar()
        week_number = str(today_date[1]).zfill(2) + str(today_date[0])

        schedule = ltc.getFormattedSchedule(week_number)
        ltc.updateCalendar(schedule)
        
        print("Week " + str(week_number) + " updated (current). " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - Waiting " + str(current_week_sync_interval*60) + "s...")
        sleep(current_week_sync_interval*60)

def updateFutureWeeks():
    ltc = lectioToCalendar(user_name, password, school_id, calendar_id)
    i_week = 1
    
    while True:
        future_date = (datetime.today()+timedelta(weeks=i_week)).isocalendar()
        week_number = str(future_date[1]).zfill(2) + str(future_date[0])

        schedule = ltc.getFormattedSchedule(week_number)
        ltc.updateCalendar(schedule)
        
        if i_week >= sync_weeks_ahead:
            i_week = 0
        i_week+=1
        
        print("Week " + str(week_number) + " updated (future).  " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - Waiting " + str(future_week_sync_interval*60) + "s...")
        sleep(future_week_sync_interval*60)

def main():
    print("Server 'LectioToCalendar' started...")

    current_week_thread = threading.Thread(target=updateCurrentWeek)
    future_weeks_thread = threading.Thread(target=updateFutureWeeks)
    
    current_week_thread.start()
    future_weeks_thread.start()
        
if __name__ == '__main__':
    main()