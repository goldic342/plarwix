from pydantic import BaseModel, Field, field_validator

from utils.validators import check_is_alpha


class SClasCreate(BaseModel):
    number: int
    letter: str =  Field(min_length=1, max_length=1)

    _is_alpha = field_validator("letter")(check_is_alpha)
