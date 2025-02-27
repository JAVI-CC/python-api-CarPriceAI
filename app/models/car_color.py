from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..db import Base


class CarColor(Base):
  __tablename__ = "car_colors"

  id = Column(String(150), primary_key=True)
  name = Column(String(150), nullable=False, unique=True)

  car_predictions = relationship("CarPrediction", back_populates="car_color")
