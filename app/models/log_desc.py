from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..db import Base


class LogDesc(Base):
  __tablename__ = "log_descs"

  id = Column(String(150), primary_key=True)
  description = Column(String(255), nullable=False, unique=True)

  logs = relationship("Log", back_populates="log_desc")
