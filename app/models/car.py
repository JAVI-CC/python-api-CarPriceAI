from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer, String
from ..db import Base


class Car(Base):
  __tablename__ = "cars"

  id = Column(String(150), primary_key=True)
  brand = Column(String(255), nullable=False)
  model = Column(String(255), nullable=False)
  fuel = Column(String(255), nullable=False)
  year = Column(Integer, CheckConstraint('year <= 9999'), nullable=False)  # 4 digits
  mileage = Column(Integer, CheckConstraint('mileage <= 9999999'), nullable=False)  # 7 digits
  horsepower = Column(Integer, CheckConstraint('horsepower <= 9999'), nullable=False)  # 4 digits
  doors = Column(Integer, CheckConstraint('doors <= 9'), nullable=False)  # 1 digits
  transmission = Column(String(255), nullable=False)
  color = Column(String(255), nullable=False)
  is_dealer = Column(Boolean, nullable=False)
  price = Column(Integer, CheckConstraint('price <= 999999'), nullable=False)  # 6 digits
  date = Column(DateTime, nullable=False)