from pydantic import (BaseModel, Field)


class CarTransmissionBase(BaseModel):
  id: str
  name: str = Field(min_length=1, max_length=150)


class CarTransmissionCreate(CarTransmissionBase):
  pass


class CarTransmission(CarTransmissionBase):

  class Config:
    from_attributes = True
