
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import sessionmaker
import os,logging

from app.entity import Base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger(__name__)

class DBConnect:

    __instance = None
    __engine_created = None

    def __new__(cls):
        if cls.__instance is None :
            cls.__instance = super().__new__(cls)
        return  cls.__instance   

    def __init__(self):

        if not self.__class__.__engine_created:

            self.engine=None
            self.Session=None
            self.create_dbengine()
            if self.engine and self.Session:
                self.__class__.__engine_created = True

    # Engine Setup
    def create_dbengine(self):

        try:
            DB_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
            # connect_args={"check_same_thread": False} : Tells SQLite, Allow this connection to be used across multiple threads.
            self.engine = create_engine(DB_URI,connect_args={"check_same_thread": False}) # IMP: to make SQLite connections to be shared across threads
            Base.metadata.create_all(self.engine)
            SS= sessionmaker(bind=self.engine)
            self.Session = SS
            logger.info("SUCCESS: DB session ")
            print("SUCCESS: DB session ")
        except Exception as ex:
            self.engine=None
            self.Session=None
            print ('Db_ENGINE create issue..')
            logger.error('Db_ENGINE create issue..')
            print(repr(ex))

