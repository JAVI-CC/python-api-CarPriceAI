from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..schemas import CarFuel as SchemaCarFuel
from ..services import get_fuels
from ..db import get_db
from ..core import (limiter, LIMIT_VALUE)


router = APIRouter(
    prefix="/fuels",
    tags=["fuel"],
    responses={
        status.HTTP_404_NOT_FOUND: {"message": f"{'fuel_not_found'}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.get("/", response_model=list[SchemaCarFuel])
@limiter.limit(LIMIT_VALUE)
async def show_fuels(request: Request, db: Session = Depends(get_db)):
  fuels = get_fuels(db)
  return fuels
