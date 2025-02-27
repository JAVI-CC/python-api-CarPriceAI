from pydantic import BaseModel, Field


class LogMetricBase(BaseModel):
  # id: str # Optional
  name: str = Field(min_length=1, max_length=255)
  score: float
  log_id: str


class LogMetric(LogMetricBase):
  class Config:
    from_attributes = True
