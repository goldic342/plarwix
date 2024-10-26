from pydantic import BaseModel, Field, field_validator

from utils.validators import check_is_alpha


class SSubjectCreate(BaseModel):
    name: str = Field(min_length=1)

    _is_alpha = field_validator("name")(check_is_alpha)
