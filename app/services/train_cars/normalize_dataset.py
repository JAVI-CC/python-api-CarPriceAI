import pickle
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from pandas import DataFrame
from ...enums.storage_path import StoragePath as EnumStoragePath
from ...enums.columns_car import ColumnsCar as EnumColumnsCar


def scaling_numeric_data(cars_df: DataFrame) -> DataFrame:
  num_cols = EnumColumnsCar.SCALER.value
  file_path = f'{EnumStoragePath.TRAIN_CARS.value}/scalers.pkl'
  scalers = {}

  for column in num_cols:
    scaler = MinMaxScaler()
    cars_df[column] = scaler.fit_transform(cars_df[column].values.reshape(-1, 1))
    scalers[column] = scaler

  with open(file_path, 'wb') as f:
    pickle.dump(scalers, f)

  return cars_df


def scaling_categorical_data(cars_df: DataFrame) -> DataFrame:
  cat_cols = EnumColumnsCar.ENCODER.value
  file_path = f'{EnumStoragePath.TRAIN_CARS.value}/encoders.pkl'
  encoders = {}

  for column in cat_cols:
    encoder = LabelEncoder()
    cars_df[column] = encoder.fit_transform(cars_df[column])
    encoders[column] = encoder

  with open(file_path, 'wb') as f:
    pickle.dump(encoders, f)

  return cars_df
