'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from base_storage import BaseStorage

class DBBackend(BaseStorage):
    '''
    Proof-of-concept to simulate DB queries
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
