from abc import ABC
from app.utils.db_operation import DBConnect

# Just to integrate DbLayer
class BaseService(ABC):

    def __init__(self):
        self.db=DBConnect()

