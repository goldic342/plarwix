from subject.model import SubjectModel
from core.mongodb_service import BaseMongoService
from subject.repository import SubjectRepository


class SubjectService(BaseMongoService):
    repository = SubjectRepository
    return_model = SubjectModel