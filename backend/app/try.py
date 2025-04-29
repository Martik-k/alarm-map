from datetime import datetime
from zoneinfo import ZoneInfo
def get_kyiv_time():
    now_kyiv = datetime.now(ZoneInfo("Europe/Kyiv"))
    return now_kyiv.replace(tzinfo=None)

print(get_kyiv_time())
