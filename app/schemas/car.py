from typing import Optional
from pydantic import BaseModel


class CarBase(BaseModel):
  pass


class CarQuestionHistory(CarBase):
  question: str
  answer: str


class CarQuestion(CarBase):
  question: str
  chat_history: Optional[list[CarQuestionHistory]]  = None


class CarAnswer(CarBase):
  answer: str
  chat_history: Optional[list[CarQuestionHistory]]  = None
