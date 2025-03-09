import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import numpy as np
from ...db import engine
from ...enums.storage_path import StoragePath as EnumStoragePath


def get_cars_recommended(car_scaling_data):
  from ...services import get_all_cars_df

  with open(f'{EnumStoragePath.TRAIN_CARS.value}/scaled_data.pkl', 'rb') as file:
    cars_scaled_data = pickle.load(file)

  pca = PCA(n_components=3)

  cars_scaled_data_pca = pca.fit_transform(cars_scaled_data)
  
  car_scaling_data_pca = pca.transform(car_scaling_data)

  similarity_scores = cosine_similarity(car_scaling_data_pca, cars_scaled_data_pca)

  similar_car_indices = np.argsort(similarity_scores[0])[::-1][:5]

  cars_df = get_all_cars_df(engine)

  cars_recommended = cars_df.iloc[similar_car_indices]

  return cars_recommended
