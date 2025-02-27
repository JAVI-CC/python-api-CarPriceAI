from uuid import uuid4
from sqlalchemy.orm import Session
from ..models import LogMetric as ModelLogMetric
from ..schemas import LogMetric as SchemaLogMetric


def create_log_metrics(db: Session, log_metrics: list[SchemaLogMetric]) -> None:

  for metric in log_metrics:
    db_metric = ModelLogMetric(
        **metric.model_dump(),
        id=uuid4()
    )

    db.add(db_metric)
