'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from base_storage import BaseStorage

class DBStorage(BaseStorage):
    '''
    Proof-of-concept to simulate DB queries
    Abstract methods which should be overridden
    can handle DB queries like insert, selects and update etc.
    '''

    ENGINE_NAME = 'db_storage'

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
