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
        Inherited from Person
        '''
        super(Candidate).__init__(name)

