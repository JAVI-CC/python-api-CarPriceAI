from os import path
import pickle
from sklearn.neighbors import NearestNeighbors
from ...db import engine
from ...enums.storage_path import StoragePath as EnumStoragePath

FILE_PATH = f'{EnumStoragePath.TRAIN_CARS.value}/model_recommended.pkl'


def training_model_recommended(training_data):
  model = None

  if path.isfile(FILE_PATH):
    with open(FILE_PATH, 'rb') as file:
      model = pickle.load(file)
  else:
    model = NearestNeighbors(n_neighbors=5)

  model.fit(training_data)

  with open(FILE_PATH, 'wb') as file:
    pickle.dump(model, file)


def get_cars_recommended(car_data_scaling):
  from ...services import get_all_cars_df

  with open(FILE_PATH, 'rb') as file:
    knn = pickle.load(file)

  _, indices = knn.kneighbors(car_data_scaling)

  cars_df = get_all_cars_df(engine)

  cars_recommended = cars_df.iloc[indices[0]]

  return cars_recommended
