from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from ..db import Base


class Log(Base):
  __tablename__ = "logs"

  id = Column(String(150), primary_key=True)
  date = Column(DateTime, nullable=False)
  log_desc_id = Column(String(150), ForeignKey("log_descs.id"))
  user_id = Column(String(150), ForeignKey("users.id"))

  log_desc = relationship("LogDesc", back_populates="logs", lazy='subquery')
  user = relationship("User", back_populates="logs", lazy='subquery')
  log_metrics = relationship("LogMetric", back_populates="log")
