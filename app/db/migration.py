from sqlalchemy.exc import SQLAlchemyError
# from ..models import User, LogDesc, Log, CarBrand, LogImage, LogMetric,
# CarModel, CarFuel, CarTransmission, CarColor, CarPrediction, Car
from ..db import engine, Base
from ..seeders import SeederUsers, SeederLogDescs
from ..core import delete_files_by_path
from ..enums.storage_path import StoragePath

try:
  Base.metadata.drop_all(bind=engine)
except SQLAlchemyError as e:
  pass

Base.metadata.create_all(bind=engine)

SeederUsers()
SeederLogDescs()

delete_files_by_path(StoragePath.TRAIN_CARS.value)
delete_files_by_path(StoragePath.CHROMA_DB.value)
