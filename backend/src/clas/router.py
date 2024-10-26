import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from auth.depends import get_current_superuser
from task.service import TaskService
from user_clas.service import UserClasService
from clas.schemas import SClasCreate
from clas.model import ClasModel
from config import settings
from clas.service import ClasService


router = APIRouter(prefix="/class")

if settings.ENVIRONMENT != "test":
    router.dependencies = [Depends(get_current_superuser)]


@router.get("/id/{clas_id}", response_model=ClasModel)
async def get_clas_by_id(clas_id: uuid.UUID):
    return await ClasService.get_by_id(clas_id)


@router.get("/all", response_model=list[ClasModel])
async def get_all_clases():
    return await ClasService.get_all()


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_clas(clas: SClasCreate):
    await ClasService.add(clas, {"number": clas.number, "letter": clas.letter})
    return JSONResponse({"message": "Class was created succesfully!"})


@router.put("/update/{clas_id}")
async def update_clas(clas_id: uuid.UUID, clas: SClasCreate):
    await ClasService.update(clas, clas_id)
    return JSONResponse({"message": "Class was updated succesfully!"})


@router.delete("/delete/{clas_id}")
async def delete_clas(clas_id: uuid.UUID):
    await ClasService.delete(clas_id)
    await UserClasService.delete_by_clas_id(clas_id)
    await TaskService.delete_tasks_by_clas_id(clas_id)
    return JSONResponse({"message": "Class was deleted succesfully!"})
