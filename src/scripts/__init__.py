from calendar_app.calendar_entry import CalendarEntry, EntryConstructor


def ctor():
    ctor = EntryConstructor.from_json()
    ctor.loop()

if __name__ == "__main__":
    ctor()
