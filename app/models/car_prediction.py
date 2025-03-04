from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base


class CarPrediction(Base):
  __tablename__ = "car_predictions"

  id = Column(String(150), primary_key=True)
  year = Column(Integer, CheckConstraint('year <= 9999'), nullable=False)  # 4 digits
  mileage = Column(Integer, CheckConstraint('mileage <= 9999999'), nullable=False)  # 7 digits
  horsepower = Column(Integer, CheckConstraint('horsepower <= 9999'), nullable=False)  # 4 digits
  doors = Column(Integer, CheckConstraint('doors <= 9'), nullable=False)  # 1 digits
  is_dealer = Column(Boolean, nullable=False)
  price = Column(Integer, CheckConstraint('price <= 999999'), nullable=False)  # 6 digits
  date = Column(DateTime, nullable=False)
  car_brand_id = Column(String(150), ForeignKey("car_brands.id"))
  car_model_id = Column(String(150), ForeignKey("car_models.id"))
  car_fuel_id = Column(String(150), ForeignKey("car_fuels.id"))
  car_transmission_id = Column(String(150), ForeignKey("car_transmissions.id"))
  car_color_id = Column(String(150), ForeignKey("car_colors.id"))

  car_brand = relationship("CarBrand", back_populates="car_predictions", lazy='subquery')
  car_model = relationship("CarModel", back_populates="car_predictions", lazy='subquery')
  car_fuel = relationship("CarFuel", back_populates="car_predictions", lazy='subquery')
  car_transmission = relationship("CarTransmission", back_populates="car_predictions", lazy='subquery')
  car_color = relationship("CarColor", back_populates="car_predictions", lazy='subquery')
