from sqlalchemy.orm import Session
from ..models import CarFuel as ModelCarFuel
from ..schemas import CarFuelCreate as SchemaFuelCreate


def get_fuel(db: Session, fuel_id: str):
  return db.query(ModelCarFuel
                  ).filter(ModelCarFuel.id == fuel_id).first()


def get_fuels(db: Session):
  return db.query(ModelCarFuel).order_by(ModelCarFuel.name).all()


def get_fuel_by_name(db: Session, fuel_name: str):
  return db.query(ModelCarFuel
                  ).filter(ModelCarFuel.name == fuel_name).first()


def create_fuel(db: Session, fuel: SchemaFuelCreate) -> None:

  db_fuel = ModelCarFuel(
      **fuel.model_dump()
  )

  db.add(db_fuel)
