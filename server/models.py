from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class Articles(BaseModel):
    title: str
    subTitle: str
    article: str


class Clothes(BaseModel):
    grade: str
    region: str
    price: Decimal
    product: str

