from pydantic import (BaseModel, Field)


class CarColorBase(BaseModel):
  id: str
  name: str = Field(min_length=1, max_length=150)


class CarColorCreate(CarColorBase):
  pass


class CarColor(CarColorBase):
  class Config:
    from_attributes = True
