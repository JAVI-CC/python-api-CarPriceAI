from pydantic import (BaseModel, Field)


class CarFuelBase(BaseModel):
  id: str
  name: str = Field(min_length=1, max_length=150)


class CarFuelCreate(CarFuelBase):
  pass


class CarFuel(CarFuelBase):

  class Config:
    from_attributes = True
