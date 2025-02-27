from enum import Enum


class ColumnsCar(Enum):
  ALL = ['brand', 'model', 'fuel', 'year', 'doors', 'transmission',
             'is_dealer', 'color', 'mileage', 'horsepower', 'price']
  ENCODER = ['brand', 'model', 'fuel', 'year', 'doors', 'transmission', 'is_dealer', 'color']
  SCALER = ['mileage', 'horsepower', 'price']
  STR = ['brand', 'model', 'fuel', 'transmission', 'color']
