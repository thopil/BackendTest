'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from base_storage import BaseStorage

class DBStorage(BaseStorage):
    '''
    Proof-of-concept to simulate DB queries
    '''

    ENGINE_NAME = 'db_storage'

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
