from dataclasses import dataclass
from calendar_app.parser import get_tokens
from calendar_app.consts import APP_DIR, DEFAULT_CONSTRUCTOR_STATE
import json
from datetime import datetime as dt_datetime
import dateutil.parser as dtp


@dataclass(init=False)
class CalendarEntry:
    """
    This class represent something that can be marked in a physical calendar. Combination of date, hour, place and note.

    Attributes:
        datetime: date and time of event
        duration: duration of event (in minutes)
        note: user created note about this event
        periodicity: how often event will occur
    """

    datetime: dt_datetime
    duration: int
    periodicity: str
    note: str

    def __init__(self, datetime: str, duration: int, periodicity: str, note: str) -> None:
        self.datetime = dtp.parse(datetime)
        self.duration = duration
        self.periodicity = periodicity
        self.note = note

    def to_dict(self):
        _d = {kw: self.__getattribute__(kw) for kw in ["duration", "periodicity", "note"]}
        _d["datetime"] = self.datetime.strftime("%d.%m.%Y, %H:%M")
        return _d

    def save(self):
        """
        Save entry to system.
        """
        with open(f"{APP_DIR}/calendar_data.json", "r", encoding="utf-8") as data_file:
            try:
                data = json.load(data_file)
            except json.decoder.JSONDecodeError:
                if input("Data corrupted. Delete it? y/n ").lower() == "y":
                    data = []
                else:
                    raise KeyboardInterrupt

        data.append(self.to_dict())

        with open(f"{APP_DIR}/calendar_data.json", "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, indent=4)



@dataclass()
class EntryConstructor:
    """
    This class tracks state of the program allowing for efficient entry construction.

    There should be 2 ways of controlling EntryConstructor:
    1) loop: upon starting program you enter a loop where you can modify constructor however you like (note: no sys.argv ie expected there)
    2) cli command: upon calling, creates instance of EntryConstructor and has it perform something, then saves it to .calendar/constructor_state.json
    """

    _datetime: str = DEFAULT_CONSTRUCTOR_STATE["datetime"]
    _duration: int  = DEFAULT_CONSTRUCTOR_STATE["duration"]
    _periodicity: str  = DEFAULT_CONSTRUCTOR_STATE["periodicity"]
    _note: str = DEFAULT_CONSTRUCTOR_STATE["note"]

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
    
    def datetime(self, new_datetime: str, *args):
        self._datetime = new_datetime

    def duration(self, new_duration: str, *args):
        self._duration = int(new_duration)

    def periodicity(self, new_periodicity: str, *args):
        self._periodicity = new_periodicity

    def note(self, new_note: str, *args):
        self._note = new_note

    def show(self, *args):
        print(self.__repr__())

    def dump(self):
        return CalendarEntry(datetime=self._datetime, duration=self._duration, periodicity=self._periodicity, note=self._note)

    def reset(self):
        """
        Make constructor state default.
        """
        for key, val in DEFAULT_CONSTRUCTOR_STATE.items():
            self.__setattr__("_" + key, val)

    def loop(self):
        """
        This method is meant to be called by looping script.
        """

        allowed_attrs = ["datetime", "duration", "periodicity", "note", "create", "show", "reset"]

        while True:

            print(f"Current state: {self}.")
            user_input = input(">> ")
            args = get_tokens(user_input)
            try:
                cmd = args[0]
                if cmd in allowed_attrs:
                    result = self.__getattribute__(cmd)(*args[1:])
                else:
                    raise AttributeError(f"Cannot call {cmd}.")
                if cmd.lower() == "create":
                    print(f"Created {result}.")
                    break
            except AttributeError as e:
                print(e)
                continue

    def create(self, *args):
        """
        This method builds CalendarEntry from settings of a EntryCOnstructor. It is meant to be called by cli tool, not loop.

        If parameters are not set before calling create(), then this method uses sys.argv in the following way:
        len(args) == 0 -> just make entry
        len(args) == 1 -> args[0] -> note
        len(args) == 2 -> args[0] -> datetime, args[1] -> note
        len(args) == 3 -> args[0] -> datetime, args[1] -> duration, args[2] -> note
        len(args) == 4 -> args[0] -> datetime, args[1] -> duration, args[2] -> periodicity, args[3] -> note 
        """
        if len(args) == 0:
            calendar_entry = self.dump()
            calendar_entry.save()
            return calendar_entry
        
        note = args[-1]
        args = args[:-1]
        keywords = ["datetime", "duration", "periodicity"]
        kwargs = {kw: arg for kw, arg in zip(keywords, args)}
        _kwargs = {kw: kwargs.get(kw, self.__getattribute__("_" + kw)) for kw in keywords}
     
        calendar_entry = CalendarEntry(note=note, **_kwargs)
        calendar_entry.save()
        return calendar_entry
