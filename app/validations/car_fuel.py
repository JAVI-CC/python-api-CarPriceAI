from sqlalchemy.orm import Session
from ..db import engine
from ..services import get_fuel


def car_fuel_id_exists(fuel_id: str):
  with Session(engine) as db:
    if not get_fuel(db, fuel_id):
      raise ValueError("car_fuel_id_not_exists")
    return fuel_id
