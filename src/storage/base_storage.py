'''
Created on 12 Oct 2018

@author: thomaspilz
'''
from singleton import Singleton
from abc import ABCMeta, abstractmethod
from datetime import datetime


class BaseStorage(Singleton, metaclass=ABCMeta):
    '''
    Base class for all storages
    '''

    def __init__(self, engine_name):
        '''
        BaseStorage, doing nothing
        implemented as singleton
        '''
        self.engine_name = engine_name

    @classmethod
    def check_name(cls, engine_name):
        '''

        :param cls:
        :param engine_name:
        '''
        return engine_name == cls.ENGINE_NAME

    @abstractmethod
    def get_all_slots(self):
        pass

    def _get_range_intersections(self, interviewer, requests, duration, f_slots):
        sorted_slots = sorted(f_slots)
        available_slots = []
        for start, end in sorted_slots:
            assert start <= end
            while start + duration <= end:
                start_duration = start + duration
                for request in requests:
                    #if request[0] >= start and request[1] <= start_duration:
                    #if request[0] < start_duration and request[1] >= start:
                    if max(request[0], start) < min(request[1], start_duration):
                        available_slots.append((start, start_duration))
                        print("{:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S} {}".format(start, start_duration, interviewer.name))

                start += duration

        return available_slots

    def _format_time_ranges(self, slots):
        dt_format = '%Y-%m-%d %H:%M:%S'
        return [(datetime.strptime(slot[0], dt_format),
                 datetime.strptime(slot[1], dt_format)) for slot in slots]
