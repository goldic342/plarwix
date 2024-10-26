from pydantic import BaseModel
from database import BaseMongo


class SubjectModel(BaseMongo):
    name: str
