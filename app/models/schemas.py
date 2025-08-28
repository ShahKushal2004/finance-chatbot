from pydantic import BaseModel, Field # type: ignore
from typing import Optional
from datetime import date

class ChatRequest(BaseModel):
    query: str = Field(..., example="How much did I spend on food last month?")

class UploadResponse(BaseModel):
    message: str
    rows: int

class Transaction(BaseModel):
    date: date
    description: str
    amount: float
    category: Optional[str] = None
