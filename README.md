This extension of **Lectio Scraper**, embeds Lectio events into Google Calendar using [this api](https://developers.google.com/calendar/api).

## Preparation
Start by [creating a new project](https://console.cloud.google.com/projectcreate) at Google Cloud console. Enable the Calendar API, go to credentials, and create an OAuth 2.0 client (then download the new credentials.json file into the *src* folder).<br><br>
If you don't want to use your primary calender, get a list over all of your ID's using [service.calendarList()](https://developers.google.com/calendar/api/v3/reference/calendarList/list). Default value of *calendarId* i "primary".



## Usage Example

```python
from calendar import lectioToCalendar

ltc = lectioToCalendar(lectioUsername, lectioPassword, schoolId, calendarId)
schedule1 = ltc.getFormattedSchedule("512022") # Format: WWYYYY

ltc.updateCalendar(schedule1)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
