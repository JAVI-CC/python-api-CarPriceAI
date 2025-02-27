from fastapi import APIRouter, status, Request, Depends
from sqlalchemy.orm import Session
from ..services import create_car_prediction
from ..schemas import (CarPrediction as SchemaCarPrediction,
                       CarPredictionValidation as SchemaCarPredictionValidation)
from ..db import get_db
from ..core import (limiter, LIMIT_VALUE)
from ..validations import validate_is_trained_data

router = APIRouter(
    prefix="/car_prediction",
    tags=["car_prediction"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "message": f"{'could_not_validate_credentials'}"
        },
        status.HTTP_404_NOT_FOUND: {"message": f"{'user_not_found'}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.post(
    "/",
    response_model=SchemaCarPrediction,
    dependencies=[
      Depends(validate_is_trained_data),
    ],
)
@limiter.limit(LIMIT_VALUE)
async def car_prediction_price(
    request: Request,
    car_prediction: SchemaCarPredictionValidation,
    db: Session = Depends(get_db),
):

  car_prediction = create_car_prediction(db, car_prediction)

  return car_prediction
