from calendar_app.calendar_entry import EntryConstructor
import dotenv


def setup():
    import os
    import json

    dotenv.load_dotenv()
    APP_DIR = os.environ["APP_DIR"]
    try:
        os.makedirs(APP_DIR)
        with open(f"{APP_DIR}/constructor_state.json", "w") as f:
            data = {"datetime": "01.10.1999",
                    "duration": 60,
                    "periodicity": "once",
                    "note": ""}
            json.dump(data, f, indent=4)
    except OSError:
        if "constructor_state.json" in os.listdir(APP_DIR):
            with open(f"{APP_DIR}/constructor_state.json", "r") as f:
                try:
                    temp_data = json.load(f)
                except json.decoder.JSONDecodeError:
                    temp_data = {}
                data = {"datetime": temp_data.get("datetime", "01.10.1999"),
                    "duration": temp_data.get("duration", 60),
                    "periodicity": temp_data.get("periodicity", "once"),
                    "note": temp_data.get("note", "")}
                
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
    ctor = EntryConstructor.from_json()
    ctor.loop()


def cli():
    """Update saved state or create new entry"""
    import sys

    args = sys.argv[1:]
    ctor = EntryConstructor.from_json()
    ctor.__getattribute__(args[0])(*args[1:])

    try:
        ctor.save()
    except EntryConstructor.BreakLoop:
        pass


if __name__ == "__main__":
    setup()
