from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from ..services import get_count_cars_trained
from ..db import engine


def validate_car_csv_file(file: UploadFile):
  file_size = 20000000  # 20MB
  accepted_file_types = ["text/csv"]

  if file.content_type not in accepted_file_types:
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=f"{'unsupported_file_type'}",
    )

  if file.size > file_size:
    raise HTTPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail=f"{'too_large'}"
    )

  return True


def validate_is_trained_data():
  if get_count_cars_trained(Session(engine)) <= 0:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"{'In_order_to_access_it_first_the_data_must_be_trained'}"
    )

  return True
