'''
Created on 12 Oct 2018

@author: thomaspilz
'''

class Slot(object):
    '''
    classdocs
    '''

    def __init__(self, begin, end):
        '''
        @params begin datetime
        @params end datetime
        '''
        self.begin = begin
        self.end   = end

    def __eq__(self, other):
        """
        Two slots are equal if their datetimes of begin and end are equal
        """
        return (self.begin[0] == other.begin[0] and self.end[0] == other.end[1])
