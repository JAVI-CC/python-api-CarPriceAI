from ..db import engine, Base
# from ..models import User, LogDesc, Log, CarBrand, LogImage, LogMetric,
# CarModel, CarFuel, CarTransmission, CarColor, CarPrediction, Car
from ..seeders import SeederUsers, SeederLogDescs

Base.metadata.create_all(bind=engine)

SeederUsers()
SeederLogDescs()
