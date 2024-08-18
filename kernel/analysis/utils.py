from typing import Literal
from pydantic import BaseModel


class StructureSchema(BaseModel):
    product_id: str
    product_name: str
    feedback_level: Literal['positive', 'negative', 'neutral']
    feedback_text: str
    feedback_translated: str
    feedback_language: str
    user_rate: int
    user_race: str
    user_gender: str
    user_occupation: str
    user_age: str
    advantages: list[str]
    disadvantages: list[str]
    suggestions: list[str]
    date_utc: str
    sentiment: float
