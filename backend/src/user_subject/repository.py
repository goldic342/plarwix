from user_subject.schemas import SUserSubject
from core.mongodb_repository import BaseMongoRepository
from database import mongo_db

class UserSubjectRepository(BaseMongoRepository):
    collection = mongo_db.subject_user

    @classmethod
    async def get_subjects_by_user_id(cls, user_id: str) -> list[SUserSubject]:
        try:
            result = cls.collection.aggregate([
                {
                    "$match": {"user_id": user_id}
                },
                {
                    "$lookup": {
                        "from": "subject",
                        "localField": "subject_id",
                        "foreignField": "_id",
                        "as": "subjectDetails"
                    }
                },
                {
                    "$unwind": "$subjectDetails"
                },
                {
                    "$project": {
                        "_id": 0,
                        "id": "$subjectDetails._id",
                        "name": "$subjectDetails.name"
                    }
                }
            ])
            return await result.to_list()
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def add_user_subjects(cls, user_id: str, subjects_ids: set[str]):
        try:
            await cls.collection.insert_many([{"user_id": user_id, "subject_id": id} for id in subjects_ids])
        except Exception as e:
            cls.handle_db_error(e)
    
    @classmethod
    async def delete_by_subject_id(cls, subject_id: str):
        try:
            await cls.collection.delete_many({"subject_id": subject_id})
        except Exception as e:
            cls.handle_db_error(e)

    @classmethod
    async def delete_by_user_id(cls, user_id: str):
        try: 
            await cls.collection.delete_many({"user_id": user_id})
        except Exception as e:
            cls.handle_db_error(e)