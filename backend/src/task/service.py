import uuid
from task.schemas import STaskCreate
from core.mongodb_service import BaseMongoService
from task.repository import TaskRepository
from task.model import TaskModel

class TaskService(BaseMongoService):
    repository = TaskRepository
    return_model = TaskModel

    @classmethod
    async def add(cls, task: STaskCreate, user_id: uuid.UUID):
        task = TaskModel(user_id=str(user_id), **task.model_dump())
        await cls.repository.add(task)

    @classmethod
    async def get_tasks_by_clas_id(cls, clas_id: uuid.UUID) -> list[TaskModel]:
        return await cls.repository.get_tasks_by_clas_id(str(clas_id))
    
    @classmethod
    async def get_tasks_by_user_id(cls, user_id: uuid.UUID) -> list[TaskModel]:
        return await cls.repository.get_tasks_by_user_id(str(user_id))
    
    @classmethod
    async def delete_tasks_by_clas_id(cls, clas_id: uuid.UUID):
        await cls.repository.delete_tasks_by_clas_id(str(clas_id))
    
    @classmethod
    async def delete_tasks_by_user_id(cls, user_id: uuid.UUID):
        await cls.repository.delete_tasks_by_user_id(str(user_id))