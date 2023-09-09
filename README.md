This fork of [**LectioScraper**](https://github.com/fredrikj31/LectioScraper), adds your Lectio events to Google Calendar using [the Google Calendar API](https://developers.google.com/calendar/api).

## Preparation
Start by [creating a new project](https://console.cloud.google.com/projectcreate) at Google Cloud console. Enable the Calendar API, go to credentials, and create an OAuth 2.0 client (then download the credentials.json file into your main script folder, eg. *server*). You will be prompted with a Google login screen first time running the script.<br><br>
If you don't want to use your primary calender for your Lectio events, get a list over all of your calendars' ID using [service.calendarList()](https://developers.google.com/calendar/api/v3/reference/calendarList/list). If you *do* want your default calender to be used, ```calendarId``` should be "primary".

The contents of the JSON object in `abbreviations.json` should be of following formatting:

```json
{
    "Actual abbreviation": "Desired Title"
}
```

Where the key `"Actual abbreviation"` is the title of the team (eg `"2a Fy"`), and the value `"Desired Title"` is the title that you want in your Google Calendar. If no abbreviations for a given module is found, it will default to the actual title of that module.


## Usage Example

```python
from calendar import lectioToCalendar

ltc = lectioToCalendar(lectioUsername, lectioPassword, schoolId, calendarId)
schedule1 = ltc.getFormattedSchedule("512022") # Format: WWYYYY

ltc.updateCalendar(schedule1)
```

## The Server
This repository also includes a [server](/server/), that can be hosted to always keep your calendar up to date. You can tune the server to your needs by changing variables, controlling how often it should be updating and how many weeks into the future it should update.

## License
[MIT](https://choosealicense.com/licenses/mit/)
