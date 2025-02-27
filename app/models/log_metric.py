from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.types import DECIMAL as Decimal
from sqlalchemy.orm import relationship
from ..db import Base


class LogMetric(Base):
  __tablename__ = "log_metrics"

  id = Column(String(150), primary_key=True)
  name = Column(String(255), nullable=False)
  score = Column(Decimal(20, 18), nullable=False)
  log_id = Column(String(150), ForeignKey("logs.id"))

  log = relationship("Log", back_populates="log_metrics", lazy='subquery')
