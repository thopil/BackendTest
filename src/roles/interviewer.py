'''
Created on 12 Oct 2018

@author: tp
'''
from .person import Person


class Interviewer(Person):
    '''
    Interviewer class inherited from Person
    '''


    def __init__(self, name):
        '''
        Inherited from Person
        '''
        super().__init__(name)
