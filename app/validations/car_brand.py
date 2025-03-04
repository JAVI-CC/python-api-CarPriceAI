from sqlalchemy.orm import Session
from ..db import engine
from ..services import get_brand


def car_brand_id_exists(brand_id: str):
  with Session(engine) as db:
    if not get_brand(db, brand_id):
      raise ValueError("car_brand_id_not_exists")
    return brand_id
