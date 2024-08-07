import datetime
from source import Source, Skola24Source
from calendar_api import CalendarApi
from update_calendar import update_calendar

import yaml
from yaml.loader import SafeLoader


class Calendar:
    """
    Helper class for matching a Skola24 calendar with a Google Calendar.

    If [calendar_id] is not specified, tries to automatically determine it based on [name]
    """
    calendarApi: CalendarApi = CalendarApi()

    def __init__(self, source: Source, calendar_id: str | None = None, name: str | None = None) -> None:

        self.name = name if name != None else f"Schema ({skola24_id})"
        
        self.source: Source = source
        self.calendar_id = calendar_id if calendar_id != None else \
            self.calendarApi.get_calendar_id(self.name)

    def update(self, year: int, week: int):
        """
        Update all lessons during the specified [week] and [year], so that the Google Calendar matches the Skola24 calendar.
        """
        update_calendar(self.source, self.calendar_id, year,
                        week, self.calendarApi)

    def __repr__(self) -> str:
        return f"Calendar({self.name}, skola24_id: {self.skola24_id}, google_calendar_id: {self.calendar_id})"


if __name__ == '__main__':
    with open('calendars.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

    Calendar.calendarApi = CalendarApi()

    weeks_to_sync = 4 if not "weeks_to_sync" in data else data["weeks_to_sync"]

    calendars = [Calendar(Skola24Source(data["domain"], data["school"], data["calendars"][name]["id"]), name=name)
                 for name in data["calendars"]]

    for calendar in calendars:
        print(f"===== {calendar.name} =====")

        now = datetime.datetime.now().isocalendar()
        for week in range(now.week, now.week+weeks_to_sync):
            calendar.update(now.year, week)

        print("\n")
