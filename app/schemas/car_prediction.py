from importlib import import_module
from datetime import datetime
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import (BaseModel, Field,
                      field_validator,
                      computed_field)
from ..core.date_formatter import date_format_server_to_client
from ..schemas.car import Car as SchemaCar

# Order columns important!
class CarPredictionBase(BaseModel):
  brand: str = Field(min_length=1, max_length=150)
  model: str = Field(min_length=1, max_length=150)
  fuel: str = Field(min_length=1, max_length=50)
  year: int = Field(min=1900, max=3000)
  mileage: int = Field(min=0, max=9999999)
  horsepower: int = Field(min=1, max=9999)
  doors: int = Field(min=1, max=9)
  transmission: str = Field(min_length=1, max_length=50)
  color: str = Field(min_length=1, max_length=150)
  is_dealer: bool | None = Field(default=True)


class CarPredictionValidation(CarPredictionBase):
  pass


class CarPredictionCreate(BaseModel):
  id: str
  year: int
  mileage: int
  horsepower: int
  doors: int
  is_dealer: bool
  price: int
  date: datetime
  car_brand_id: str
  car_model_id: str
  car_fuel_id: str
  car_transmission_id: str
  car_color_id: str

  @field_validator("car_brand_id")
  @classmethod
  def car_brand_id_exists(cls, brand_id: str):
    validator = import_module("app.validations.car_brand")
    return validator.car_brand_id_exists(brand_id)

  @field_validator("car_model_id")
  @classmethod
  def car_model_id_exists(cls, model_id: str, info: FieldValidationInfo):
    validator = import_module("app.validations.car_model")
    return validator.car_model_id_exists(info.data['car_brand_id'], model_id)

  @field_validator("car_fuel_id")
  @classmethod
  def car_fuel_id_exists(cls, fuel_id: str):
    validator = import_module("app.validations.car_fuel")
    return validator.car_fuel_id_exists(fuel_id)

  @field_validator("car_transmission_id")
  @classmethod
  def car_transmission_id_exists(cls, transmission_id: str):
    validator = import_module("app.validations.car_transmission")
    return validator.car_transmission_id_exists(transmission_id)

  @field_validator("car_color_id")
  @classmethod
  def car_color_id_exists(cls, color_id: str):
    validator = import_module("app.validations.car_color")
    return validator.car_color_id_exists(color_id)


class CarPrediction(BaseModel):
  price: float
  date: datetime
  cars_recommended: list[SchemaCar]

  @computed_field
  @property
  def date_format(self) -> datetime:
    return date_format_server_to_client(str(self.date))

  class Config:
    from_attributes = True
