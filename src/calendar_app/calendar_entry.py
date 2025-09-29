from dataclasses import dataclass
import sys
from calendar_app.consts import APP_DIR
import json


@dataclass()
class CalendarEntry:
    """
    This class represent something that can be marked in a physical calendar. Combination of date, hour, place and note.

    Attributes:
        datetime: date and time of event
        duration: duration of event (in minutes)
        note: user created note about this event
        periodicity: how often event will occur
    """

    datetime: str
    duration: int
    periodicity: str
    note: str

    def to_dict(self):
        return {
            kw: self.__getattribute__(kw) for kw in ["datetime", "duration", "periodicity", "note"]   
        }

    def save(self):
        """
        Save entry to system.
        """
        with open(f"{APP_DIR}/calendar_data.json", "a", encoding="utf-8") as data_file:
            json.dump(self.to_dict(), data_file, indent=4)


@dataclass()
class EntryConstructor:
    """
    This class tracks state of the program allowing for efficient entry construction.
    """

    _datetime: str | None = None
    _duration: int | None = 60
    _periodicity: str | None = "weekly"
    _note: str | None = None

    def set_datetime(self, new_datetime: str):
        self._datetime = new_datetime
    
    def set_duration(self, new_duration: str):
        self._duration = int(new_duration)

    def set_periodicity(self, new_periodicity: str):
        self._periodicity = new_periodicity

    def set_note(self, new_note: str):
        self._note = new_note

    def show(self, *args):
        print(self.__repr__())

    def create(self):
        """
        This method builds CalendarEntry from settings of a EntryCOnstructor.

        If parameters are not set before calling create(), then this method uses sys.argv in the following way:
        sys.argv[1] -> datetime
        sys.argv[2] -> if there is no sys.argv[3] then make it a note else make it duration
        sys.argv[3] -> note if exists
        """

        # here are some settings that JUST make sense
        datetime = self._datetime if self._datetime is not None else sys.argv[1]
        if len(sys.argv) <= 3:
            duration = self._duration
            note = sys.argv[2]
        else:
            duration = int(sys.argv[2])
            note = sys.argv[3]

        calendar_entry = CalendarEntry(datetime=datetime, duration=duration, periodicity=self._periodicity, note=note) #type: ignore
        calendar_entry.save()
        return calendar_entry
