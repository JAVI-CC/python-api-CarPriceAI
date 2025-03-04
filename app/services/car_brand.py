from sqlalchemy.orm import Session
from ..models import CarBrand as ModelCarBrand
from ..schemas import CarBrandCreate as SchemaBrandCreate


def get_brand(db: Session, brand_id: str):
  return db.query(ModelCarBrand
                  ).filter(ModelCarBrand.id == brand_id).first()


def get_brand_by_name(db: Session, brand_name: str):
  return db.query(ModelCarBrand
                  ).filter(ModelCarBrand.name == brand_name).first()


def get_brands(db: Session):
  return db.query(ModelCarBrand).order_by(ModelCarBrand.name).all()


def create_brand(db: Session, brand: SchemaBrandCreate) -> None:

  db_brand = ModelCarBrand(
      **brand.model_dump()
  )

  db.add(db_brand)
