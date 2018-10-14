'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from person import Person

class Interviewer(Person):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        super(Interviewer).__init__(name)
        self.__slots = []

    def get_slots(self):
        return self.__slots

    def set_slots(self, value):
        self.__slots = value

    def del_slots(self):
        del self.__slots

    def add_slot(self, slot):
        self.__slots.append(slot)

    slots = property(get_slots, set_slots, del_slots, "slots's docstring")
