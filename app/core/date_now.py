from zoneinfo import ZoneInfo
from datetime import datetime
from ..core import getenv


def generate_date_now() -> datetime:
  return datetime.now(ZoneInfo(getenv("TIMEZONE"))
                      ).strftime("%Y-%m-%d %H:%M:%S")
