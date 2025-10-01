from calendar_app.calendar_entry import EntryConstructor
from calendar_app.my_calendar import Calendar
from calendar_app.consts import DEFAULT_CONSTRUCTOR_STATE, APP_DIR


def setup():
    import os
    import json

    try:
        os.makedirs(APP_DIR)
        with open(f"{APP_DIR}/constructor_state.json", "w") as f:
            json.dump(DEFAULT_CONSTRUCTOR_STATE, f, indent=4)
    except OSError:
        if "constructor_state.json" in os.listdir(APP_DIR):
            with open(f"{APP_DIR}/constructor_state.json", "r") as f:
                try:
                    temp_data = json.load(f)
                except json.decoder.JSONDecodeError:
                    temp_data = {}
                data = {"datetime": temp_data.get("datetime", DEFAULT_CONSTRUCTOR_STATE["datetime"]),
                    "duration": temp_data.get("duration", DEFAULT_CONSTRUCTOR_STATE["duration"]),
                    "periodicity": temp_data.get("periodicity", DEFAULT_CONSTRUCTOR_STATE["periodicity"]),
                    "note": temp_data.get("note", DEFAULT_CONSTRUCTOR_STATE["note"])}
                
            with open(f"{APP_DIR}/constructor_state.json", "w") as f:
                json.dump(data, f, indent=4)
        else:
            with open(f"{APP_DIR}/constructor_state.json", "w") as f:
                pass

    with open(f"{APP_DIR}/calendar_data.json", "a"):
        pass


def ctor():
    """Start loop for creating entry or modifying state"""
    setup()
    ctor = EntryConstructor()
    ctor.loop()


def cli_ctor(args=None):
    """Update saved state or create new entry"""
    import sys

    _args = args if args is not None else sys.argv[1:]
    ctor = EntryConstructor.from_json()
    result = ctor.__getattribute__(_args[0])(*_args[1:])
    if result is not None:
        print(result)
    ctor.save()


def cli():
    """Integrated cli""" 

    # setup
    import sys

    args = sys.argv[1:]
    try:
        cmd = args[0]
    except IndexError:
        print("No cmd")
        return
    

    if cmd == "setup":
        setup()
        return
    
    if cmd == "ctor":
        ctor()
        return
    
    if cmd == "day":
        calendar = Calendar()
        calendar.show(*args[1:])
        return

    ctor_cmds = ["create", "reset", "show", "datetime", "duration", "periodicity", "note"]
    if cmd in ctor_cmds:
        cli_ctor(args=args)
        return
    

if __name__ == "__main__":
    setup()
