from sqlalchemy.orm import Session
from ..db import engine
from ..services import get_model


def car_model_id_exists(brand_id: str, model_id: str):
  with Session(engine) as db:
    if not get_model(db, brand_id, model_id):
      raise ValueError("car_model_id_not_exists")
    return model_id
