from user_clas.schemas import SUserClas
from core.mongodb_repository import BaseMongoRepository
from database import mongo_db

class UserClasRepository(BaseMongoRepository):
    collection = mongo_db.class_user

    @classmethod
    async def get_clases_by_user_id(cls, user_id: str) -> list[SUserClas]:
        try:
            result = cls.collection.aggregate([
                {
                    "$match": {"user_id": user_id}
                },
                {
                    "$lookup": {
                        "from": "class",
                        "localField": "class_id",
                        "foreignField": "_id",
                        "as": "classDetails"
                    }
                },
                {
                    "$unwind": "$classDetails"
                },
                {
                    "$project": {
                        "_id": 0,
                        "id": "$classDetails._id",
                        "number": "$classDetails.number",
                        "letter": "$classDetails.letter"
                    }
                }
            ])
            return await result.to_list()
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def add_user_clases(cls, user_id: str, clases_ids: set[str]):
        try:
            await cls.collection.insert_many([{"user_id": user_id, "class_id": id} for id in clases_ids])
        except Exception as e:
            cls.handle_db_error(e)
    
    @classmethod
    async def delete_by_clas_id(cls, clas_id: str):
        try:
            await cls.collection.delete_many({"subject_id": clas_id})
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def delete_by_user_id(cls, user_id: str):
        try: 
            await cls.collection.delete_many({"user_id": user_id})
        except Exception as e:
            cls.handle_db_error(e)