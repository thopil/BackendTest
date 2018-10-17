'''
Created on 12 Oct 2018

@author: tp
'''
from memory_storage import MemoryStorage
from db_storage import DBStorage
from google_storage import GoogleCalendarStorage

class StorageFactory(object):
    '''
    Fraud Engine Factory
    '''
    STORAGE_ENGINES = [MemoryStorage, DBStorage, GoogleCalendarStorage]

    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.storage_engine = self.choose_storage_engine()

    def choose_storage_engine(self):
        for engine in self.STORAGE_ENGINES:
            if engine.check_name(self.engine_name):
                return engine(self.engine_name)

    def create_storage(self):
        return self.choose_storage_engine()
