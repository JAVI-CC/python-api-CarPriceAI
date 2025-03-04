from sqlalchemy.orm import Session
from ..db import engine
from ..services import get_transmission


def car_transmission_id_exists(transmission_id: str):
  with Session(engine) as db:
    if not get_transmission(db, transmission_id):
      raise ValueError("car_transmission_id_not_exists")
    return transmission_id
