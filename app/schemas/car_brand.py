from pydantic import (BaseModel, Field)
from .car_model import CarModel


class CarBrandBase(BaseModel):
  name: str = Field(min_length=1, max_length=150)


class CarBrandCreate(CarBrandBase):
  id: str


class CarBrand(CarBrandBase):
  id: str
  car_models: list[CarModel]

  class Config:
    from_attributes = True
