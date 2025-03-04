from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db import Base


class CarModel(Base):
  __tablename__ = "car_models"

  id = Column(String(150), primary_key=True)
  name = Column(String(150), nullable=False)
  car_brand_id = Column(String(150), ForeignKey("car_brands.id"))

  car_brand = relationship("CarBrand", back_populates="car_models", lazy='subquery')
  car_predictions = relationship("CarPrediction", back_populates="car_model")

  __table_args__ = (
      UniqueConstraint('name', 'car_brand_id', name='unique_name_car_brand_id'),
    )
