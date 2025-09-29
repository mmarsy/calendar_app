from dataclasses import dataclass
from calendar_app.parser import get_tokens
from calendar_app.consts import APP_DIR, DEFAULT_CONSTRUCTOR_STATE
import json
import sys


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

    There should be 2 ways of controlling EntryConstructor:
    1) loop: upon starting program you enter a loop where you can modify constructor however you like (note: no sys.argv ie expected there)
    2) cli command: upon calling, creates instance of EntryConstructor and has it perform something, then saves it to .calendar/constructor_state.json
    """

    _datetime: str | None = DEFAULT_CONSTRUCTOR_STATE["datetime"]
    _duration: int | None = DEFAULT_CONSTRUCTOR_STATE["duration"]
    _periodicity: str | None = DEFAULT_CONSTRUCTOR_STATE["periodicity"]
    _note: str | None = DEFAULT_CONSTRUCTOR_STATE["note"]

    @staticmethod
    def from_json():
        with open(f"{APP_DIR}/constructor_state.json", "r", encoding="utf-8") as f:
            kwargs = {"_" + key: val for key, val in json.load(f).items()}
            return EntryConstructor(**kwargs)
        
    def save(self):
        with open(f"{APP_DIR}/constructor_state.json", "w", encoding="utf-8") as f:
            data = {"datetime": self._datetime,
                    "duration": self._duration,
                    "periodicity": self._periodicity,
                    "note": self._note}
            json.dump(data, f, indent=4)

    def set_datetime(self, new_datetime: str):
        self._datetime = new_datetime
    
    def datetime(self, new_datetime: str, *args):
        self._datetime = new_datetime

    def set_duration(self, new_duration: str):
        self._duration = int(new_duration)

    def duration(self, new_duration: str, *args):
        self._duration = int(new_duration)

    def set_periodicity(self, new_periodicity: str):
        self._periodicity = new_periodicity

    def periodicity(self, new_periodicity: str, *args):
        self._periodicity = new_periodicity

    def set_note(self, new_note: str):
        self._note = new_note

    def note(self, new_note: str, *args):
        self._note = new_note

    def show(self, *args):
        print(self.__repr__())

    def reset(self):
        pass

    def loop(self):
        """
        This method is meant to be called by looping script.
        """

        allowed_attrs = ["datetime", "duration", "periodicity", "note", "create", "show", "reset"]

        while True:
            user_input = input(">> ")
            args = get_tokens(user_input)
            try:
                cmd = args[0]
                if cmd in allowed_attrs:
                    result = self.__getattribute__(cmd)(*args[1:])
                else:
                    raise AttributeError(f"Cannot call {cmd}.")
                if cmd.lower() == "create":
                    print(result)
                    break
            except AttributeError as e:
                print(e)
                continue

    def create(self, *args):
        """
        This method builds CalendarEntry from settings of a EntryCOnstructor. It is meant to be called by cli tool, not loop.

        If parameters are not set before calling create(), then this method uses sys.argv in the following way:
        sys.argv[2] -> datetime
        sys.argv[3] -> if there is no sys.argv[3] then make it a note else make it duration
        sys.argv[4] -> note if exists
        """
     
        datetime = self._datetime if self._datetime is not None else sys.argv[2]
        if len(sys.argv) <= 4:
            duration = self._duration
            note = self._note if self._duration is not None else sys.argv[3]
        else:
            duration = int(sys.argv[3])
            note = sys.argv[4]

        calendar_entry = CalendarEntry(datetime=datetime, duration=duration, periodicity=self._periodicity, note=note) #type: ignore
        calendar_entry.save()
        return calendar_entry
