from sqlalchemy.orm import Session
from ..models import (CarModel as ModelCarModel,
                      CarBrand as ModelCarBrand)
from ..schemas import CarModelCreatePrediction as SchemaModelCreatePrediction


def get_model(db: Session, brand_id: str, model_id: str):
  return db.query(ModelCarModel
                  ).filter(ModelCarModel.car_brand_id == brand_id,
                           ModelCarModel.id == model_id).first()


def get_model_by_name(db: Session, brand_id: str, model_name: str):
  return db.query(ModelCarModel
                  ).filter(ModelCarModel.car_brand_id == brand_id,
                           ModelCarModel.name == model_name).first()


def get_models(db: Session, brand_id: str):
  return db.query(ModelCarModel
                  ).filter(ModelCarModel.car_brand_id == brand_id
                           ).order_by(ModelCarModel.name).all()


def create_model_prediction(db: Session, model: SchemaModelCreatePrediction) -> None:

  db_model = ModelCarModel(
      **model.model_dump()
  )

  db.add(db_model)
