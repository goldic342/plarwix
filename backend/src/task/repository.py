from task.model import TaskModel
from database import mongo_db
from core.mongodb_repository import BaseMongoRepository

class TaskRepository(BaseMongoRepository):
    collection = mongo_db.task

    @classmethod
    async def get_tasks_by_clas_id(cls, clas_id: str) -> list[TaskModel]:
        try:
            await cls.collection.update_many({"class_id": clas_id}, {"$inc": {"views": 1}})
            return await cls.collection.find({"class_id": clas_id}).to_list()
        except Exception as e:
            cls.handle_db_error(e)
    
    @classmethod
    async def get_tasks_by_user_id(cls, user_id: str) -> list[TaskModel]:
        try:
            await cls.collection.update_many({"user_id": user_id}, {"$inc": {"views": 1}})
            return await cls.collection.find({"user_id": user_id}).to_list()
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def delete_tasks_by_clas_id(cls, clas_id: str):
        try:
            await cls.collection.delete_many({"class_id": clas_id})
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def delete_tasks_by_user_id(cls, user_id: str):
        try:
            await cls.collection.delete_many({"user_id": user_id})
        except Exception as e:
            cls.handle_db_error(e)
    