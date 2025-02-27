import asyncio
from datetime import datetime
from random import randint
from uuid import uuid4
from sqlalchemy.orm import Session
from pandas import DataFrame
from .train_cars import (structure_columns,
                         null_data_handling,
                         delete_duplicates_based_db,
                         scaling_numeric_data,
                         scaling_categorical_data,
                         division_data_training_and_test,
                         training_model,
                         validation_model,
                         delete_rows_alredy_exists_db)
from ..core import generate_date_now, ConnectionManager
from ..models import (Car,
                      CarBrand,
                      CarModel,
                      CarColor,
                      CarTransmission,
                      CarFuel)
from ..enums.log_desc import LogDesc as EnumLogDesc
from ..schemas import (Log as SchemaLog,
                       LogMetric as SchemaLogMetric)
from ..services.log import create_log
from ..services.log_metric import create_log_metrics


async def training_cars(db: Session,
                        user_id: str,
                        cars_df: DataFrame,
                        connection_manager: ConnectionManager):
  ### Phase 2: Data exploration and preparation ###
  await connection_manager.send_personal_message({'message': 'DATA_EXPLORATION_AND_PREPARATION',
                                                  'percentage': randint(11, 20)}, user_id)

  cars_df, cars_scaling_df = await asyncio.to_thread(data_exploration_preparation, cars_df)

  # Check if the dataset is empty
  if not cars_df.empty:
    ### Phase 3: Training and testing data splitting ###
    await connection_manager.send_personal_message({'message': 'TRAINING_AND_TESTING_SPLITTING',
                                                    'percentage': randint(21, 30)}, user_id)
    x_train, x_test, y_train, y_test = division_data_training_and_test(cars_scaling_df)

    ### Phase 4: Model training and predictions ###
    await connection_manager.send_personal_message({'message': 'MODEL_TRAINING_AND_PREDICTIONS',
                                                    'percentage': randint(31, 50)}, user_id)
    predictions = await asyncio.to_thread(training_model, x_train, x_test, y_train)

    ### Phase 5: Model validation ###
    await connection_manager.send_personal_message({'message': 'MODEL_VALIDATION',
                                                    'percentage': randint(51, 60)}, user_id)
    metrics_dict = validation_model(y_test, predictions)

    # Check if the dataset has no new records to insert into the database
    await connection_manager.send_personal_message({'message': 'CHECKING_DATA',
                                                    'percentage': randint(61, 80)}, user_id)
    cars_df = delete_rows_alredy_exists_db(cars_df)

    date_now = generate_date_now()

    # Insert BBDD
    if not cars_df.empty:
      await connection_manager.send_personal_message({'message': 'INSERT_NEW_RECORDS',
                                                      'percentage': randint(81, 90)}, user_id)
      insert_train_cars(db, cars_df, date_now)
      insert_car_brands(db)
      insert_car_models(db)
      insert_car_colors(db)
      insert_car_fuels(db)
      insert_car_transmissions(db)

    generate_logs(db, user_id, metrics_dict, date_now)

    db.commit()

  await connection_manager.send_personal_message({'message': 'FINALIZED',
                                                  'percentage': 100}, user_id)


def data_exploration_preparation(cars_df: DataFrame) -> DataFrame:

  # Detect automatic columns
  dict_columns, del_columns = structure_columns(cars_df.columns.values.tolist())

  cars_df = cars_df.drop(del_columns, axis=1)

  cars_df.rename(columns=dict_columns, inplace=True)

  # Delete duplicates
  cars_df.drop_duplicates(inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  # Detect null values
  cars_df = null_data_handling(cars_df)

  # Delete duplicates
  cars_df.drop_duplicates(inplace=True)
  cars_df = cars_df.reset_index(drop=True)

  # Detect and drop duplicates based database
  cars_df = delete_duplicates_based_db(cars_df, True)

  # Data normalization techniques.
  cars_scaling_df = cars_df.copy()
  if not cars_df.empty:
    cars_scaling_df = scaling_numeric_data(cars_scaling_df)
    cars_scaling_df = scaling_categorical_data(cars_scaling_df)

  return cars_df, cars_scaling_df


def insert_train_cars(db: Session, cars_df: DataFrame, date_now: datetime):
  cars_df['date'] = date_now
  cars_df['id'] = cars_df.apply(lambda _: uuid4(), axis=1)

  cars_dict = cars_df.to_dict(orient='records')

  db.bulk_insert_mappings(Car, cars_dict)


# Get all brands not registered in table car_brands
def insert_car_brands(db: Session) -> None:
  result = db.query(Car.brand
                    ).join(CarBrand, Car.brand == CarBrand.name, isouter=True
                           ).filter(CarBrand.id == None
                                    ).group_by(Car.brand).all()

  new_brands = [{'id': uuid4(),
                 'name': car.brand} for car in result]

  db.bulk_insert_mappings(CarBrand, new_brands)


# Get all brands not registered in table car_models
def insert_car_models(db: Session) -> None:
  result = db.query(CarBrand.id, Car.model
                    ).join(CarBrand, Car.brand == CarBrand.name
                           ).join(CarModel, Car.model == CarModel.name, isouter=True
                                  ).filter(CarModel.id == None
                                           ).group_by(Car.brand, Car.model).all()

  new_models = [{'id': uuid4(),
                 'name': car.model,
                 'car_brand_id': car.id
                 } for car in result]

  db.bulk_insert_mappings(CarModel, new_models)


# Get all brands not registered in table car_colors
def insert_car_colors(db: Session) -> None:
  result = db.query(Car.color
                    ).join(CarColor, Car.color == CarColor.name, isouter=True
                           ).filter(CarColor.id == None
                                    ).group_by(Car.color).all()

  new_colors = [{'id': uuid4(),
                 'name': car.color} for car in result]

  db.bulk_insert_mappings(CarColor, new_colors)


# Get all brands not registered in table car_transmissions
def insert_car_transmissions(db: Session) -> None:
  result = db.query(Car.transmission
                    ).join(CarTransmission, Car.transmission == CarTransmission.name, isouter=True
                           ).filter(CarTransmission.id == None
                                    ).group_by(Car.transmission).all()

  new_transmissions = [{'id': uuid4(),
                        'name': car.transmission} for car in result]

  db.bulk_insert_mappings(CarTransmission, new_transmissions)


# Get all brands not registered in table car_fuels
def insert_car_fuels(db: Session) -> None:
  result = db.query(Car.fuel
                    ).join(CarFuel, Car.fuel == CarFuel.name, isouter=True
                           ).filter(CarFuel.id == None
                                    ).group_by(Car.fuel).all()

  new_fuels = [{'id': uuid4(),
                'name': car.fuel} for car in result]

  db.bulk_insert_mappings(CarFuel, new_fuels)


# Get all brands not registered in table car_fuels
def generate_logs(db: Session,
                  user_id: str,
                  metrics: list[dict],
                  date_now: datetime) -> None:

  log_dict = {
      'id': str(uuid4()),
      'date': date_now,
      'log_desc_id': EnumLogDesc.TRAIN_CARS.value,
      'user_id': user_id
  }

  log = SchemaLog(**log_dict)

  create_log(db, log)

  log_metrics = [SchemaLogMetric(**{**metric, 'log_id': log_dict['id']})
                 for metric in metrics]

  create_log_metrics(db, log_metrics)


def get_count_cars_trained(db: Session) -> int:
  return db.query(Car).count()
