import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from auth.depends import get_current_superuser
from user_clas.schemas import SUserClas
from user_clas.service import UserClasService
from config import settings

router = APIRouter()

if settings.ENVIRONMENT != "test":
    router.dependencies = [Depends(get_current_superuser)]

@router.post("/add/{user_id}/classes", status_code=status.HTTP_201_CREATED)
async def add_user_clases(user_id: uuid.UUID, clases_ids: set[uuid.UUID]):
    await UserClasService.add_user_clases(user_id, clases_ids)
    return JSONResponse({"message": "Classes to user succesfully added!"})

@router.get("/{user_id}/classes", response_model=list[SUserClas])
async def get_clases_by_user_id(user_id: uuid.UUID):
    return await UserClasService.get_clases_by_user_id(user_id)

@router.put("/update/{user_id}/classes")
async def update_user_clases(user_id: uuid.UUID, clases_ids: set[uuid.UUID]):
    await UserClasService.update_user_clases(user_id, clases_ids)
    return JSONResponse({"message": "Classes to user succesfully updated!"})