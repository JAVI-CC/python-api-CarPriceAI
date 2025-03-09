from fastapi import Depends, APIRouter, status, Request
from sqlalchemy.orm import Session
from ..schemas import CarColor as SchemaCarColor
from ..services import get_colors
from ..db import get_db
from ..core import (limiter, LIMIT_VALUE)


router = APIRouter(
    prefix="/colors",
    tags=["color"],
    responses={
        status.HTTP_404_NOT_FOUND: {"message": f"{'color_not_found'}"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "message": f"{'internal_server_error'}"
        },
    },
)


@router.get("/", response_model=list[SchemaCarColor])
@limiter.limit(LIMIT_VALUE)
async def show_colors(request: Request, db: Session = Depends(get_db)):
  colors = get_colors(db)
  return colors
