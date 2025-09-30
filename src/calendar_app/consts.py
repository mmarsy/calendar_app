import os
import datetime
import dotenv


dotenv.load_dotenv()


APP_DIR = os.environ["APP_DIR"]
DATE_FMT = os.environ["DATE_FMT"]

DEFAULT_CONSTRUCTOR_STATE = {
    "datetime": datetime.datetime.now().strftime("%d/%m/%y %H:%M"),
    "duration": 60,
    "periodicity": "once",
    "note": "",
}

PERIODICITY = {
    "weekly": lambda d1, d2: d1.weekday() == d2.weekday(),
    "daily": lambda d1, d2: True,
    "annualy": lambda d1, d2: d1.month == d2.month and d1.day == d2.day
}
