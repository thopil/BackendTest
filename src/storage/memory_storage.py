'''
Created on 12 Oct 2018

@author: tp
'''
import threading
import numpy as np
from datetime import timedelta, datetime
from functools import reduce

from .base_storage import BaseStorage
from src.roles.interviewer import Interviewer
from src.roles.candidate import Candidate

initial_data = {
    'interviewer_1': [
        (datetime(2018, 10, 14, 9, 0), datetime(2018, 10, 14, 10, 0)),
        (datetime(2018, 10, 16, 9, 0), datetime(2018, 10, 16, 14, 0)),
        (datetime(2018, 10, 17, 11, 0), datetime(2018, 10, 17, 12, 0))
    ],
    'interviewer_2': [
        (datetime(2018, 10, 15, 10, 0), datetime(2018, 10, 15, 11, 0)),
        (datetime(2018, 10, 16, 11, 0), datetime(2018, 10, 16, 12, 0)),
        (datetime(2018, 10, 17, 10, 0), datetime(2018, 10, 17, 12, 0))
    ]
}

class MemoryStorage(BaseStorage):
    '''
    Inherited class from BaseStorage
    This storage stores all slots/candidates/interviewers in memory
    '''

    ENGINE_NAME = 'memory_storage'

    def __init__(self, engine_name):
        '''
        manages all available slots (free/blocked) in memory
        -  usually handled by relational database
        '''
        BaseStorage.__init__(self, engine_name)
        self.__slots_by_interviewer = initial_data
        self.__interviewers = [Interviewer('interviewer_1'), Interviewer('interviewer_2')]
        self.__candidates = []
        #experimental
        self.__candidates_np = dict()
        self.__interviewers_np = dict()
        self.lock = threading.Lock()

    def del_slots(self):
        del self.__slots_by_interviewer

    def del_slots_by_interviewer(self, name):
        if any(x.get_name() == name for x in self.__interviewers):
            del self.__slots_by_interviewer[name]
            interviewer = Interviewer(name)
            self.__interviewers.remove(interviewer)
            return True
        return False

    def get_interviewer(self):
        return [interviewer.name for interviewer in self.__interviewers]

    def get_slots_by_name(self, name):
        return self.__slots_by_interviewer.get(name, [])

    def get_all_slots(self):
        return self.__slots_by_interviewer.items()

    def get_free_slots(self, candidate, *interviewers):
        '''
        :param candidate: candidate who requested free slots
        :returns: intersection of slots for all requested interviewers
        '''
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

        return self._merge_slots(test_set)

    def get_free_slots_by_interviewer(self, interviewer, requests,
                                      duration=timedelta(hours=1)):
        f_slots = self.__slots_by_interviewer.get(interviewer.name)
        available_slots = self._get_range_intersections(interviewer, requests, duration, f_slots)
        return available_slots

    def set_slots(self, data_slots):
        for name, slots in data_slots.items():
            interviewer = Interviewer(name)
            self.set_slots_by_interviewer(interviewer, slots)

    def set_slots_by_interviewer(self, interviewer, slots):
        '''
        set a new slot
        needs to be thread-safe
        :param identifier: key to identify slot
        :param slot: free slot
        '''
        if interviewer in self.__interviewers:
            return False

        new_slots = self._format_time_ranges(slots)
        with self.lock:
            self.__slots_by_interviewer[interviewer.name] = new_slots
            self.__interviewers.append(interviewer)

    def update_slots_by_interviewer(self, name, slots):
        '''
        update a new slot for a given interviewer
        needs to be thread-safe
        :param identifier: key to identify slot
        :param slot: free slot
        '''
        if not any(x.get_name() == name for x in self.__interviewers):
            return False

        new_slots = self._format_time_ranges(slots)
        with self.lock:
            self.__slots_by_interviewer[name] = new_slots

        return True

    def already_exists(self, name):
        if name in self.__interviewers:
            return True


    #-- experimental approach
    def _create_slots_array(self, slots):
        '''
        create numpy array for each hour in the datetime range
        '''
        slot_array = np.array([])
        for slot in slots:
            begin, end = slot
            arr = np.array([(begin + timedelta(hours=i), begin + timedelta(hours=i+1)) for i in range(end.hour-begin.hour)])
            slot_array = np.concatenate((slot_array, arr))
        return slot_array

    def _create_np_container(self, input_data):
        container = {}
        for name, slots in input_data.items():
            new_slots = self._format_time_ranges(slots)
            container[name] = self._create_slots_array(new_slots)
        return container

    def get_free_slots_np(self, candidates_list, interviewer_list):
        candidate_slots   = [candidate.get_slots() for candidate in self.__candidates_np.values() if candidate.get_name() in candidates_list]
        interviewer_slots = [interviewer.get_slots() for interviewer in self.__interviewers_np.values() if interviewer.get_name() in interviewer_list]
        slots = interviewer_slots + candidate_slots

        result = reduce(np.intersect1d, slots)
        return result

    def set_free_slots_np(self, candidate_data, interviewer_data):
        interviewer_dict = self._create_np_container(interviewer_data)
        for name, slots in interviewer_dict.items():
            interviewer = Interviewer(name)
            interviewer.set_slots(slots)
            self.__interviewers_np[name] = interviewer

        candidates_dict = self._create_np_container(candidate_data)
        for name, slots in candidates_dict.items():
            candidate = Candidate(name)
            candidate.set_slots(slots)
            self.__candidates_np[name] = candidate


    slots = property(get_all_slots, set_slots, del_slots, "slots's docstring")
