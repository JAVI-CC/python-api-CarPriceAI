from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..schemas import CarTransmission as SchemaCarTransmission
from ..services import get_transmissions
from ..db import get_db
from ..core import (limiter, LIMIT_VALUE)


router = APIRouter(
    prefix="/transmissions",
    tags=["transmission"],
    responses={
        status.HTTP_404_NOT_FOUND: {"message": f"{'transmission_not_found'}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.get("/", response_model=list[SchemaCarTransmission])
@limiter.limit(LIMIT_VALUE)
async def show_transmissions(request: Request, db: Session = Depends(get_db)):
  transmissions = get_transmissions(db)
  return transmissions
