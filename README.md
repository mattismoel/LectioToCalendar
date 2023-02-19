This fork of **LectioScraper**, adds your Lectio events to Google Calendar using [this api](https://developers.google.com/calendar/api).

## Preparation
Start by [creating a new project](https://console.cloud.google.com/projectcreate) at Google Cloud console. Enable the Calendar API, go to credentials, and create an OAuth 2.0 client (then download the credentials.json file into the *src* folder). You will be prompted with a Google login screen first time running the script.<br><br>
If you don't want to use your primary calender for your Lectio events, get a list over all of your calendar ID's using [service.calendarList()](https://developers.google.com/calendar/api/v3/reference/calendarList/list). If you do want your default calender to be used, ```calendarId``` should be "primary".



## Usage Example

```python
from calendar import lectioToCalendar

ltc = lectioToCalendar(lectioUsername, lectioPassword, schoolId, calendarId)
schedule1 = ltc.getFormattedSchedule("512022") # Format: WWYYYY

ltc.updateCalendar(schedule1)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
