from sqlalchemy.orm import Session
from ..models import CarColor as ModelCarColor
from ..schemas import CarColorCreate as SchemaColorCreate


def get_color(db: Session, color_id: str):
  return db.query(ModelCarColor
                  ).filter(ModelCarColor.id == color_id).first()


def get_color_by_name(db: Session, color_name: str):
  return db.query(ModelCarColor
                  ).filter(ModelCarColor.name == color_name).first()


def get_colors(db: Session):
  return db.query(ModelCarColor).order_by(ModelCarColor.name).all()


def create_color(db: Session, color: SchemaColorCreate) -> None:

  db_color = ModelCarColor(
      **color.model_dump()
  )

  db.add(db_color)
