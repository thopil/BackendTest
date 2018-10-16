'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from roles.person import Person


class Candidate(Person):
    '''
    Candidate class inherited from Person
    '''

    def __init__(self, name):
        '''
        Inherited from Person
        '''
        super().__init__(name)
        self.__requested_slots = None

    def get_requested_slots(self):
        return self.__requested_slots

    def set_requested_slots(self, slots):
        self.__requested_slots = slots

    def del_requested_slots(self):
        del self.__requested_slots

    requested_slots = property(get_requested_slots, set_requested_slots, del_requested_slots, "requested_slots's docstring")

