from uuid import uuid4
import pickle
from sqlalchemy.orm import Session
from sqlalchemy import desc
import numpy as np
from ..models import CarPrediction as ModelCarPrediction
from ..schemas import (
    CarPredictionValidation as SchemaCarPredictionValidation,
    CarPredictionCreate as SchemaCarPredictionCreate,
    CarBrandCreate as SchemaCarBrandCreate,
    CarModelCreatePrediction as SchemaCarModelCreatePrediction,
    CarTransmissionCreate as SchemaCarTransmissionCreate,
    CarFuelCreate as SchemaCarFuelCreate,
    CarColorCreate as SchemaCarColorCreate,
    CarPrediction as SchemaCarPrediction,
)
from ..enums.storage_path import StoragePath as EnumStoragePath
from ..enums.columns_car import ColumnsCar as EnumColumnsCar
from .car_brand import create_brand, get_brand_by_name
from .car_model import create_model_prediction, get_model_by_name
from .car_fuel import create_fuel, get_fuel_by_name
from .car_color import create_color, get_color_by_name
from .car_transmission import create_transmission, get_transmission_by_name
from ..core import generate_date_now


def get_car_predictions(db: Session):
  return db.query(ModelCarPrediction).order_by(desc(ModelCarPrediction.date)).all()


def create_car_prediction(
        db: Session, car_prediction: SchemaCarPredictionValidation) -> SchemaCarPrediction:

  with open(f'{EnumStoragePath.TRAIN_CARS.value}/scalers.pkl', 'rb') as file:
    scalers = pickle.load(file)

  car_prediction_transform = transform_data(db, scalers, car_prediction)

  # Scaler data
  with open(f'{EnumStoragePath.TRAIN_CARS.value}/model.pkl', 'rb') as file:
    model = pickle.load(file)

  price_prediction = model.predict(np.array([list(car_prediction_transform.model_dump().values())]))

  price = round(scalers['price'].inverse_transform(price_prediction.reshape(-1, 1))[0][0])

  # Apply changes to BBDD
  db.commit()

  # Insert car_predicction
  car_prediction_id = uuid4()
  car_brand = get_brand_by_name(db, car_prediction.brand)
  car_model = get_model_by_name(db, car_brand.id, car_prediction.model)
  car_fuel = get_fuel_by_name(db, car_prediction.fuel)
  car_transmission = get_transmission_by_name(db, car_prediction.transmission)
  car_color = get_color_by_name(db, car_prediction.color)

  car_prediction = {
    'id': str(car_prediction_id),
    'year': car_prediction.year,
    'mileage': car_prediction.mileage,
    'horsepower': car_prediction.horsepower,
    'doors': car_prediction.doors,
    'is_dealer': car_prediction.is_dealer,
    'price': price,
    'date': generate_date_now(),
    'car_brand_id': car_brand.id,
    'car_model_id': car_model.id,
    'car_fuel_id': car_fuel.id,
    'car_transmission_id': car_transmission.id,
    'car_color_id': car_color.id,
  }

  car_prediction = SchemaCarPredictionCreate(**car_prediction)

  db_car_prediction = ModelCarPrediction(
      **car_prediction.model_dump(),
  )

  db.add(db_car_prediction)
  db.commit()
  db.refresh(db_car_prediction)

  return db_car_prediction


def transform_data(
        db: Session,
        scalers,
        car_prediction: SchemaCarPredictionValidation) -> SchemaCarPredictionCreate:

  # Scaler data
  car_prediction_transform = car_prediction.model_copy()

  car_prediction_transform.mileage = float(
    scalers['mileage'].transform([[car_prediction_transform.mileage]])[0][0])

  car_prediction_transform.horsepower = float(
    scalers['horsepower'].transform([[car_prediction_transform.horsepower]])[0][0])

  # Encoder data
  with open(f'{EnumStoragePath.TRAIN_CARS.value}/encoders.pkl', 'rb') as file:
    encoders = pickle.load(file)

  for name_col in EnumColumnsCar.ENCODER.value:
    val = getattr(car_prediction_transform, name_col)

    try:
      transform_val = int(encoders[name_col].transform([val])[0])
    except (ValueError, TypeError):
      transform_val = -1

    setattr(car_prediction_transform, name_col, transform_val)

  # Insert data if it does not exist.
  brand_id = None
  brand_name = car_prediction.brand
  car_brand_get = get_brand_by_name(db, car_prediction.brand)
  if not car_brand_get:
    brand_id = uuid4()
    brand_name = None
    insert_car_brand(db, brand_id, car_prediction.brand)

  if not car_brand_get:
    insert_car_model(db, car_prediction.model, brand_id, None)
  elif not get_model_by_name(db, car_brand_get.id, car_prediction.model):
    insert_car_model(db, car_prediction.model, None, brand_name)

  if not get_fuel_by_name(db, car_prediction.fuel):
    insert_car_fuel(db, car_prediction.fuel)

  if not get_transmission_by_name(db, car_prediction.transmission):
    insert_car_transmission(db, car_prediction.transmission)

  if not get_color_by_name(db, car_prediction.color):
    insert_car_color(db, car_prediction.color)

  return car_prediction_transform


def insert_car_brand(db: Session, brand_id: str, brand: str) -> None:
  car_brand = {
      'id': str(brand_id),
      'name': brand
  }

  car_brand = SchemaCarBrandCreate(**car_brand)

  create_brand(db, car_brand)


def insert_car_model(db: Session, model: str, brand_id: str | None, brand_name: str | None) -> None:

  if not brand_id:
    brand = get_brand_by_name(db, brand_name)
    brand_id = brand.id

  model_id = uuid4()
  car_model = {
      'id': str(model_id),
      'name': model,
      'car_brand_id': str(brand_id)
  }

  car_model = SchemaCarModelCreatePrediction(**car_model)

  create_model_prediction(db, car_model)


def insert_car_fuel(db: Session, fuel: str) -> None:
  fuel_id = uuid4()
  car_fuel = {
      'id': str(fuel_id),
      'name': fuel
  }

  car_fuel = SchemaCarFuelCreate(**car_fuel)

  create_fuel(db, car_fuel)


def insert_car_transmission(db: Session, transmission: str) -> None:
  transmission_id = uuid4()
  car_transmission = {
      'id': str(transmission_id),
      'name': transmission
  }

  car_transmission = SchemaCarTransmissionCreate(**car_transmission)

  create_transmission(db, car_transmission)


def insert_car_color(db: Session, color: str) -> None:
  color_id = uuid4()
  car_color = {
      'id': str(color_id),
      'name': color
  }

  car_color = SchemaCarColorCreate(**car_color)

  create_color(db, car_color)
