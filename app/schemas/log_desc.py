from pydantic import BaseModel, Field


class LogDescBase(BaseModel):
  id: str
  description: str = Field(min_length=3, max_length=255)


class LogDescCreateSeeder(LogDescBase):
  pass


class LogDesc(LogDescBase):
  class Config:
    from_attributes = True
