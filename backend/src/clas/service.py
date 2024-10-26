from clas.repository import ClasRepository
from clas.model import ClasModel
from core.mongodb_service import BaseMongoService


class ClasService(BaseMongoService):
    repository = ClasRepository
    return_model = ClasModel