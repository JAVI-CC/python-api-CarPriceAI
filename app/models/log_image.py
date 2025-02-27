from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from ..db import Base


class LogImage(Base):
  __tablename__ = "log_images"

  id = Column(String(150), primary_key=True)
  date = Column(DateTime, nullable=False)
  car_brand_id = Column(String(150), ForeignKey("car_brands.id"))
  user_id = Column(String(150), ForeignKey("users.id"))

  car_brand = relationship("CarBrand", back_populates="log_images", lazy='subquery')
  user = relationship("User", back_populates="log_images", lazy='subquery')
