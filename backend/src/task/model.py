from datetime import datetime, timezone
from enum import Enum

from pydantic import ConfigDict, Field, field_serializer
from database import BaseMongo

class AssignmentType(str, Enum):
    TEXT = "text"

class TaskModel(BaseMongo):
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S")})

    user_id: str
    class_id: str
    assignment_type: AssignmentType = Field(default=AssignmentType.TEXT)
    views: int = Field(default=0)
    content: str
    due_date: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    edited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

