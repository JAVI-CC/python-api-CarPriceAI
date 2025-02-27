from datetime import datetime
from pydantic import BaseModel


class LogBase(BaseModel):
  id: str
  date: datetime
  log_desc_id: str
  user_id: str


class Log(LogBase):
  class Config:
    from_attributes = True
