from typing import Annotated
from random import randint
from fastapi import BackgroundTasks, APIRouter, status, UploadFile, Request, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
from ..services import training_cars
from ..schemas import (User as SchemaUser,
                       CarQuestion as SchemaCarQuestion,
                       CarAnswer as SchemaCarAnswer)
from ..db import get_db
from ..core import (get_current_active_user,
                    csv_find_encoding_and_delimiter,
                    limiter,
                    LIMIT_VALUE,
                    connection_manager,
                    get_chat_answer)
from ..validations import validate_car_csv_file, validate_is_trained_data

router = APIRouter(
    prefix="/cars",
    tags=["car"],
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
    "/train",
    response_description="message",
    dependencies=[
      Depends(get_current_active_user),
      Depends(validate_car_csv_file)
    ],
)
@limiter.limit(LIMIT_VALUE)
async def train_dataset_cars(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: Annotated[
        SchemaUser, Depends(get_current_active_user)
    ],
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

  await connection_manager.send_personal_message({'message': 'READING_THE_DATA',
                                                  'percentage': randint(1, 10)}, current_user.id)

  contents = await file.read(1024)
  charset, dilimiter = csv_find_encoding_and_delimiter(contents)
  await file.seek(0)

  ### Phase 1: Data collection ###
  cars_df = pd.read_csv(file.file,
                        delimiter=dilimiter,
                        encoding=charset)

  cars_df = background_tasks.add_task(training_cars, db,
                                      current_user.id, cars_df, connection_manager)

  return {"message":
          f"{'The training process is underway. It may take several minutes, please wait.'}"}


@router.post(
    "/chat/question",
    response_model=SchemaCarAnswer,
    dependencies=[
      Depends(validate_is_trained_data),
    ],
)
@limiter.limit(LIMIT_VALUE)
async def car_prediction_price(
    request: Request,
    ask: SchemaCarQuestion,
):

  answer = get_chat_answer(ask.question, ask.chat_history)

  return answer
