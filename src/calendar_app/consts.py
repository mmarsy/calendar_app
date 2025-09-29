import os
import datetime
import dotenv


dotenv.load_dotenv()


APP_DIR = os.environ["APP_DIR"]
DEFAULT_CONSTRUCTOR_STATE = {
    "datetime": datetime.datetime.now().strftime("%d/%m/%y %H:%M"),
    "duration": 60,
    "periodicity": "once",
    "note": "",
}
