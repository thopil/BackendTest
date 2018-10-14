'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from base_storage import BaseStorage
from datetime import timedelta, datetime


class SlotPool(BaseStorage):
    '''
    Inherited class from BaseStorage
    '''

    ENGINE_NAME = 'slot_pool'

    def __init__(self, engine_name):
        '''
        manages all available slots (free/blocked)
        -  usually handled by relational database
        '''
        BaseStorage.__init__(self, engine_name)
        self.__slots_by_name = {}
        self.__interviewers = []

    def del_slots(self):
        del self.__slots_by_name

    def get_slots_by_name(self, name):
        return self.__slots_by_name.get(name)

    def get_all_slots(self):
        return self.__slots_by_name.items()

    def get_free_slots(self, requests, *interviewers):
        requests = self._format_time_ranges(requests)
        d = {}
        for name in self.__interviewers:
            if name in interviewers:
                free_slots = []
                free_slots.extend(self.get_free_slots_by_name(name, requests))
                d[name] = set(free_slots)

        # now find intersections of all interviewers
        # who should attend
        test_set = None
        for name, slot_set in d.items():
            if test_set is None:
                test_set = slot_set
            test_set = test_set.intersection(slot_set)

        return test_set


    def get_free_slots_by_name(self, name, requests, duration=timedelta(hours=1)):
        available_slots = []

        f_slots = self.__slots_by_name.get(name)
        slots = sorted(f_slots)

        for start, end in slots:
            assert start <= end
            while start + duration <= end:
                start_duration = start+duration
                for request in requests:
                    #print(request[0], request[1], start, start_duration)
                    if request[0] >= start and request[1] <= start_duration:
                        available_slots.append((start, start_duration))
                        print("{:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S} {}".format(start, start_duration, name))
                start += duration

        return available_slots

    def _format_time_ranges(self, slots):
        dt_format = '%Y-%m-%d %H:%M:%S'
        return [(datetime.strptime(slot[0], dt_format), datetime.strptime(slot[1], dt_format)) for slot in slots]

    def set_slots(self, data_slots):
        # JSON dict,
        # needs to be converted to datetime objects
        for name, slots in data_slots.items():
            new_slots = self._format_time_ranges(slots)
            self.__slots_by_name[name] = new_slots
            self.__interviewers.append(name)

    def set_slots_by_name(self, name, slots):
        '''
        set a new slot
        needs to be thread-safe
        @param name: key to identify slot
        @param slot: free slot
        '''
        self.__slots_by_name[name] = slots

    slots = property(get_all_slots, set_slots, del_slots, "slots's docstring")
