'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from base_storage import BaseStorage
from datetime import timedelta
from interviewer import Interviewer


class MemoryStorage(BaseStorage):
    '''
    Inherited class from BaseStorage
    This storage stores all slots/candidates/interviewers in memory
    '''

    ENGINE_NAME = 'memory_storage'

    def __init__(self, engine_name):
        '''
        manages all available slots (free/blocked)
        -  usually handled by relational database
        '''
        BaseStorage.__init__(self, engine_name)
        self.__slots_by_interviewer = {}
        self.__interviewers = []
        self.__candidates = []

    def del_slots(self):
        del self.__slots_by_interviewer

    def get_slots_by_name(self, name):
        return self.__slots_by_interviewer.get(name)

    def get_all_slots(self):
        return self.__slots_by_interviewer.items()

    def get_free_slots(self, candidate, *interviewers):
        self.__candidates.append(candidate)
        requested_slots = candidate.get_requested_slots()
        requested_slots = self._format_time_ranges(requested_slots)
        d = {}
        for name in interviewers:
            if any(x for x in self.__interviewers if x.name == name):
                interviewer = [x for x in self.__interviewers if x.name == name][0]
                free_slots = []
                free_slots.extend(self.get_free_slots_by_interviewer(interviewer, requested_slots))
                d[name] = set(free_slots)

        # now find intersections of all interviewers
        # who should attend
        test_set = None
        for name, slot_set in d.items():
            if test_set is None:
                test_set = slot_set
            test_set = test_set.intersection(slot_set)

        return test_set

    def get_free_slots_by_interviewer(self, interviewer, requests,
                                      duration=timedelta(hours=1)):
        f_slots = self.__slots_by_interviewer.get(interviewer.name)
        available_slots = self._get_range_intersections(interviewer, requests, duration, f_slots)
        return available_slots

    def set_slots(self, data_slots):
        # needs to be converted to datetime objects
        for name, slots in data_slots.items():
            interviewer = Interviewer(name)
            self.set_slots_by_interviewer(interviewer, slots)

    def set_slots_by_interviewer(self, interviewer, slots):
        '''
        set a new slot
        needs to be thread-safe
        @param name: key to identify slot
        @param slot: free slot
        '''
        new_slots = self._format_time_ranges(slots)
        self.__slots_by_interviewer[interviewer.name] = new_slots
        self.__interviewers.append(interviewer)

    slots = property(get_all_slots, set_slots, del_slots, "slots's docstring")