import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from auth.depends import get_current_superuser
from user_subject.service import UserSubjectService
from config import settings
from subject.model import SubjectModel
from subject.service import SubjectService
from subject.schemas import SSubjectCreate


router = APIRouter(prefix="/subject")

if settings.ENVIRONMENT != "test":
    router.dependencies = [Depends(get_current_superuser)]


@router.get("/id/{subject_id}")
async def get_subject_by_id(subject_id: uuid.UUID):
    return await SubjectService.get_by_id(subject_id)


@router.get("/all", response_model=list[SubjectModel])
async def get_all_subjects():
    return await SubjectService.get_all()


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SSubjectCreate):
    await SubjectService.add(subject)
    return JSONResponse({"message": "Subject was created succesfully!"})


@router.put("/update/{subject_id}")
async def update_subject(subject_id: uuid.UUID, subject: SSubjectCreate):
    await SubjectService.update(subject, subject_id)
    return JSONResponse({"message": "Subject was updated succesfully!"})


@router.delete("/delete/{subject_id}")
async def delete_subject(subject_id: uuid.UUID):
    await SubjectService.delete(subject_id)
    await UserSubjectService.delete_by_subject_id(subject_id)
    return JSONResponse({"message": "Subject was deleted succesfully!"})
