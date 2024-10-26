import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from config import settings
from auth.depends import get_current_user
from admin.model import UserBase
from task.model import TaskModel
from task.schemas import STaskCreate, STaskUpdate, STaskUpdateDate
from task.service import TaskService



router = APIRouter(prefix="/task")

if settings.ENVIRONMENT != "test":
    router.dependencies = [Depends(get_current_user)]

@router.post("/add", response_model=TaskModel, status_code=status.HTTP_201_CREATED)
async def add_task(task: STaskCreate, user: UserBase = Depends(get_current_user)):
    await TaskService.add(task, user.id)
    return JSONResponse({"message": "Task created succesfully!"})

@router.put("/update/{task_id}", response_model=TaskModel)
async def update_task(task_id: uuid.UUID, task: STaskUpdate):
    await TaskService.update(STaskUpdateDate(**task.model_dump()), task_id)
    return JSONResponse({"message": "Task updated succesfully!"})

@router.get("/class/{clas_id}", response_model=list[TaskModel])
async def get_tasks_by_clas_id(clas_id: uuid.UUID):
    return await TaskService.get_tasks_by_clas_id(clas_id)

@router.get("/user/{user_id}", response_model=list[TaskModel])
async def get_tasks_by_user_id(user_id: uuid.UUID):
    return await TaskService.get_tasks_by_user_id(user_id)

    