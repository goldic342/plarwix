from pydantic import BaseModel


class SUserSubject(BaseModel):
    id: str
    name: str