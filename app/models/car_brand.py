from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..db import Base


class CarBrand(Base):
  __tablename__ = "car_brands"

  id = Column(String(150), primary_key=True)
  name = Column(String(255), nullable=False, unique=True)

  car_models = relationship("CarModel", back_populates="car_brand")
  car_predictions = relationship("CarPrediction", back_populates="car_brand")
  log_images = relationship("LogImage", back_populates="car_brand")
