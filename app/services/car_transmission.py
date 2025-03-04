from sqlalchemy.orm import Session
from ..models import CarTransmission as ModelCarTransmission
from ..schemas import CarTransmissionCreate as SchemaTransmissionCreate


def get_transmission(db: Session, transmission_id: str):
  return db.query(ModelCarTransmission
                  ).filter(ModelCarTransmission.id == transmission_id).first()


def get_transmission_by_name(db: Session, transmission_name: str):
  return db.query(ModelCarTransmission
                  ).filter(ModelCarTransmission.name == transmission_name).first()


def get_transmissions(db: Session):
  return db.query(ModelCarTransmission).order_by(ModelCarTransmission.name).all()


def create_transmission(db: Session, transmission: SchemaTransmissionCreate) -> None:

  db_transmission = ModelCarTransmission(
      **transmission.model_dump()
  )

  db.add(db_transmission)
