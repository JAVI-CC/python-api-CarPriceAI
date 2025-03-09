from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..schemas import CarBrand as SchemaCarBrand
from ..services import get_brands
from ..db import get_db
from ..core import (limiter, LIMIT_VALUE)


router = APIRouter(
    prefix="/brands",
    tags=["brand"],
    responses={
        status.HTTP_404_NOT_FOUND: {"message": f"{'brand_not_found'}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.get("/", response_model=list[SchemaCarBrand])
@limiter.limit(LIMIT_VALUE)
async def show_brands(request: Request, db: Session = Depends(get_db)):
  brands = get_brands(db)
  return brands
