from os import path
import pickle
from pandas import DataFrame
import numpy as np
from numpy import ndarray
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (r2_score,
                             mean_squared_error,
                             mean_absolute_error)
from ...enums.storage_path import StoragePath as EnumStoragePath


def division_data_training_and_test(cars_df: DataFrame):
  x = cars_df.drop(['price'], axis=1)
  y = cars_df['price']

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

  return x_train, x_test, y_train, y_test


# It would not be necessary to save the model since the
# RandomForest algorithm does not allow incremental training.
def training_model(x_train, x_test, y_train) -> ndarray:
  file_path = f'{EnumStoragePath.TRAIN_CARS.value}/model.pkl'
  model = None

  if path.isfile(file_path):
    with open(file_path, 'rb') as file:
      model = pickle.load(file)
  else:
    model = RandomForestRegressor(random_state=42, max_features='sqrt')

  model.fit(x_train, y_train)
  model_predictions = model.predict(x_test)

  with open(file_path, 'wb') as file:
    pickle.dump(model, file)

  return model_predictions


def validation_model(y_test: list, predictions: ndarray) -> list[dict]:
  model_r2_score = r2_score(y_test, predictions)
  model_mse_score = mean_squared_error(y_test, predictions)
  model_rmse_scrore = float(np.sqrt(model_mse_score))
  model_mae_scrore = mean_absolute_error(y_test, predictions)

  return [{'name': 'R2', 'score': model_r2_score},
          {'name': 'RMSE', 'score': model_rmse_scrore},
          {'name': 'MAE', 'score': model_mae_scrore}
          ]
