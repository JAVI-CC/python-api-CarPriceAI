from ..db import engine, Base
# from ..models import User, LogDesc, Log, CarBrand, LogImage, LogMetric,
# CarModel, CarFuel, CarTransmission, CarColor, CarPrediction, Car
from ..seeders import SeederUsers, SeederLogDescs
from sqlalchemy.exc import SQLAlchemyError

try:
  Base.metadata.drop_all(bind=engine)
except SQLAlchemyError as e:
  pass

Base.metadata.create_all(bind=engine)

SeederUsers()
SeederLogDescs()
