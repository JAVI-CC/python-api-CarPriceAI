from typing import Optional
from pydantic import BaseModel


class CarBase(BaseModel):
  brand: str
  model: str
  fuel: str
  year: int
  mileage: int
  horsepower: int
  doors: int
  transmission: str
  color: str
  is_dealer: bool
  price: int


class Car(CarBase):
  pass


class CarQuestionHistory(BaseModel):
  question: str
  answer: str


class CarQuestion(BaseModel):
  question: str
  chat_history: Optional[list[CarQuestionHistory]] = None


class CarAnswer(BaseModel):
  answer: str
  chat_history: Optional[list[CarQuestionHistory]] = None
