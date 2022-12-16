This extension of **Lectio Scraper**, embeds Lectio events into Google Calendar using [this api](https://developers.google.com/calendar/api).

## Usage Example

```python
from calendar import lectioToCalendar

ltc = lectioToCalendar(lectioUsername, lectioPassword, schoolId, calendarId)
schedule1 = ltc.getFormattedSchedule("512022") # Format: WWYYYY

ltc.updateCalendar(schedule1)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
