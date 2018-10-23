'''
Created on 12 Oct 2018

@author: tp
'''

class Person(object):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.__slots = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def get_name(self):
        return self.name

    def set_slots(self, slots):
        self.__slots = slots

    def get_slots(self):
        return self.__slots
