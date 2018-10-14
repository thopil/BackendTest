'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from person import Person

class Candidate(Person):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        super(Candidate).__init__(name)
        self.__free_slots = []

    def get_slots(self):
        return self.__free_slots
