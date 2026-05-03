from datetime import datetime
import random

def get_current_timestamp() -> int:
    return int(datetime.timestamp(datetime.now()))

random.randint(10, 100)


