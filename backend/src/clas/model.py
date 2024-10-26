from sqlmodel import Field
from database import BaseMongo


class ClasModel(BaseMongo):
    number: int
    letter: str = Field(min_length=1, max_length=1)
