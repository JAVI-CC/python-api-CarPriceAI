from sqlalchemy.orm import Session
from ..db import engine
from ..services import get_color


def car_color_id_exists(color_id: str):
  with Session(engine) as db:
    if not get_color(db, color_id):
      raise ValueError("car_color_id_not_exists")
    return color_id
