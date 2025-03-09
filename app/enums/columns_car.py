from enum import Enum

# Order columns important!
class ColumnsCar(Enum):
  ALL = ['brand', 'model', 'fuel', 'year', 'mileage', 'horsepower', 'doors',
         'transmission', 'color', 'is_dealer', 'price']
  ENCODER = ['brand', 'model', 'fuel', 'year', 'doors', 'transmission', 'is_dealer', 'color']
  SCALER = ['mileage', 'horsepower', 'price']
  STR = ['brand', 'model', 'fuel', 'transmission', 'color']
  ALL_AND_ID = ['id', 'brand', 'model', 'fuel', 'year', 'mileage', 'horsepower', 'doors',
                'transmission', 'color', 'is_dealer', 'price']
