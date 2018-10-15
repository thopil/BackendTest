'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from memory_backend import MemoryStorage
from db_storage import DBStorage

class StorageFactory(object):
    '''
    Fraud Engine Factory
    '''
    STORAGE_ENGINES = [MemoryStorage, DBStorage]

    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.storage_engine = self.choose_storage_engine()

    def choose_storage_engine(self):
        for engine in self.STORAGE_ENGINES:
            if engine.check_name(self.engine_name):
                return engine(self.engine_name)

    def create_storage(self):
        return self.choose_storage_engine()
