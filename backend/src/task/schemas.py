from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, field_serializer
from task.model import AssignmentType

class STaskCreate(BaseModel):
    class_id: uuid.UUID
    assignment_type: AssignmentType = Field(default=AssignmentType.TEXT)
    content: str
    due_date: datetime

    @field_serializer("class_id")
    def serialize_id(self, id: uuid.UUID):
        return str(id)
    
class STaskUpdate(BaseModel):
    content: str
    due_date: datetime

class STaskUpdateDate(STaskUpdate):
    edited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

