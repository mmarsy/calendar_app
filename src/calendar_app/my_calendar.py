from calendar_app.calendar_entry import CalendarEntry
from calendar_app.consts import APP_DIR
from dateutil import parser as dtp
import datetime
import json


class Calendar:
    """
    Calendar class is manages saved calendar data and anwsers questions about days.

    calendar = Calendar()
    calendar.show("oct 1")
    >> CalendarEntry1, CalendarEntry2,...
    """

    _data: list[CalendarEntry]

    def __init__(self) -> None:
        with open(f"{APP_DIR}/calendar_data.json", "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = []
            self._data = []
            for entry in data:
                self._data.append(CalendarEntry(**entry))

    def show(self, string: str | None = None, *args):
        date = dtp.parse(string) if string is not None else datetime.datetime.now()
        for entry in self._data:
            if entry.compare(date):
                print(entry)


if __name__ == "__main__":
    c = Calendar()
    c.show()
