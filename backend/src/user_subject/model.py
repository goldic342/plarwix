from pydantic import BaseModel


class SubjectUserModel(BaseModel):
    subject_id: str
    user_id: str