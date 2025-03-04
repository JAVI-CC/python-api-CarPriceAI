from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..db import Base


class User(Base):
  __tablename__ = "users"

  id = Column(String(150), primary_key=True)
  name = Column(String(50), nullable=False, unique=True)
  email = Column(String(50), unique=True, nullable=False, index=True)
  hashed_password = Column(String(150), nullable=False)

  log_images = relationship("LogImage", back_populates="user", lazy='subquery')
  logs = relationship("Log", back_populates="user", lazy='subquery')
