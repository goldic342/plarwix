import uuid
from user_subject.schemas import SUserSubject
from user_subject.repository import UserSubjectRepository


class UserSubjectService:
    repository = UserSubjectRepository

    @classmethod
    async def get_subjects_by_user_id(cls, user_id: uuid.UUID) -> list[SUserSubject]:
        return await cls.repository.get_subjects_by_user_id(str(user_id))
    
    @classmethod
    async def add_user_subjects(cls, user_id: uuid.UUID, subjects_ids: set[uuid.UUID]):
        await cls.repository.add_user_subjects(str(user_id), map(str, subjects_ids))

    @classmethod
    async def update_user_subjects(cls, user_id: uuid.UUID, subjects_ids: set[uuid.UUID]):
        user_id = str(user_id)
        await cls.repository.delete_by_user_id(user_id)
        await cls.repository.add_user_subjects(user_id, map(str, subjects_ids))

    @classmethod
    async def delete_by_subject_id(cls, subject_id: uuid.UUID):
        await cls.repository.delete_by_subject_id(str(subject_id))

    @classmethod
    async def delete_by_user_id(cls, user_id: uuid.UUID):
        await cls.repository.delete_by_user_id(str(user_id))