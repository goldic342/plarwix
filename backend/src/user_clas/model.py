from pydantic import BaseModel


class ClasUserModel(BaseModel):
    class_id: str
    user_id: str