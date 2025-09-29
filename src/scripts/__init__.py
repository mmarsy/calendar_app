from calendar_app.calendar_entry import CalendarEntry, EntryConstructor


def ctor():
    ctor = EntryConstructor()
    while True:
        user_input = input().split(" ")
        if user_input[0] == "break":
            return
        ctor.__getattribute__(user_input[0])(*user_input[1:])

if __name__ == "__main__":
    ctor()
