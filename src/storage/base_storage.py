'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from singleton import Singleton
from abc import ABCMeta, abstractmethod


class BaseStorage(Singleton, metaclass=ABCMeta):
    '''
    Base class for all storages
    '''

    def __init__(self, engine_name):
        '''
        BaseStorage, doing nothing
        implemented as singleton
        '''
        self.engine_name = engine_name

    @classmethod
    def check_name(cls, engine_name):
        '''

        :param cls:
        :param engine_name:
        '''
        return engine_name == cls.ENGINE_NAME

    @abstractmethod
    def get_all_slots(self):
        pass
