from importlib import import_module
from pydantic import (BaseModel,
                      Field,
                      field_validator)


class CarModelBase(BaseModel):
  name: str = Field(min_length=1, max_length=150)


class CarModelCreatePrediction(CarModelBase):
  id: str
  car_brand_id: str


class CarModelCreate(CarModelBase):
  car_brand_id: str

  @field_validator("car_brand_id")
  @classmethod
  def car_brand_id_exists(cls, id: str):
    validator = import_module("app.validations.car_brand")
    return validator.car_brand_id_exists(id)


class CarModel(CarModelBase):
  class Config:
    from_attributes = True
