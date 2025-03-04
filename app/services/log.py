from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..models import Log as ModelLog
from ..schemas import Log as SchemaLog


def get_logs(db: Session):
  return db.query(ModelLog).order_by(desc(ModelLog.date)).all()


def create_log(db: Session, log: SchemaLog) -> None:

  db_log = ModelLog(
      **log.model_dump()
  )

  db.add(db_log)
