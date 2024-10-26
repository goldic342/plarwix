
import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from user_subject.schemas import SUserSubject
from config import settings
from auth.depends import get_current_superuser
from user_subject.service import UserSubjectService


router = APIRouter()

if settings.ENVIRONMENT != "test":
    router.dependencies = [Depends(get_current_superuser)]

@router.post("/add/{user_id}/subjects", status_code=status.HTTP_201_CREATED)
async def add_user_subjects(user_id: uuid.UUID, subjects_ids: set[uuid.UUID]):
    await UserSubjectService.add_user_subjects(user_id, subjects_ids)
    return JSONResponse({"message": "Subjects to user succesfully added!"})

@router.get("/{user_id}/subjects", response_model=list[SUserSubject])
async def get_subjects_by_user_id(user_id: uuid.UUID):
    return await UserSubjectService.get_subjects_by_user_id(user_id)

@router.put("/update/{user_id}/subjects")
async def update_user_subjects(user_id: uuid.UUID, subjects_ids: set[uuid.UUID]):
    await UserSubjectService.update_user_subjects(user_id, subjects_ids)
    return JSONResponse({"message": "Subjects to user succesfully updated!"})