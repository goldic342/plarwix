from pydantic import BaseModel


class SUserClas(BaseModel):
    id: str
    number: int
    letter: str