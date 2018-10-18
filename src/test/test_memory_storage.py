'''
Created on 14 Oct 2018

@author: tp
'''
import unittest
from datetime import datetime

from storage.storage_factory import StorageFactory
from roles.candidate import Candidate
from roles.interviewer import Interviewer


class Test(unittest.TestCase):

    def setUp(self):
        self.memory_storage = StorageFactory('memory_storage').create_storage()
        free_slots = {"Philip": [
                        ("2018-10-14 09:00:00", "2018-10-14 16:00:00"),
                        ("2018-10-15 09:00:00", "2018-10-15 16:00:00"),
                        ("2018-10-16 09:00:00", "2018-10-16 16:00:00"),
                        ("2018-10-17 09:00:00", "2018-10-17 16:00:00"),
                        ("2018-10-18 09:00:00", "2018-10-18 16:00:00"),
                        ],
                    "Sarah": [
                        ("2018-10-14 12:00:00", "2018-10-14 18:00:00"),
                        ("2018-10-15 09:00:00", "2018-10-15 12:00:00"),
                        ("2018-10-16 12:00:00", "2018-10-16 18:00:00"),
                        ("2018-10-17 09:00:00", "2018-10-17 12:00:00")
                        ],
                    "Thomas": [
                            ["2018-10-16 11:00:00", "2018-10-16 18:00:00"]
                        ]
                    }

        self.requests = [("2018-10-14 09:00:00", "2018-10-14 10:00:00"),
                    ("2018-10-15 09:00:00", "2018-10-15 10:00:00"),
                    ("2018-10-16 09:00:00", "2018-10-16 12:00:00"),
                    ("2018-10-17 09:00:00", "2018-10-17 10:00:00"),
                    ("2018-10-18 09:00:00", "2018-10-18 10:00:00"),]


        self.memory_storage.set_slots(free_slots)


    def tearDown(self):
        pass


    def test_01_get_all_slots(self):
        rtv = self.memory_storage.get_all_slots()
        #for name, slots in rtv:
        #    print(name, slots)

    def test_02__format_time_ranges(self):
        rtv = self.memory_storage._format_time_ranges(self.requests)
        assert rtv == [(datetime(2018, 10, 14, 9, 0), datetime(2018, 10, 14, 10, 0)),
                       (datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                       (datetime(2018, 10, 16, 9, 0), datetime(2018, 10, 16, 12, 0)),
                       (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0)),
                       (datetime(2018, 10, 18, 9, 0), datetime(2018, 10, 18, 10, 0))]

    def test_03_get_free_slots_by_name(self):
        requests = self.memory_storage._format_time_ranges(self.requests)
        interviewer = Interviewer('Sarah')
        rtv = self.memory_storage.get_free_slots_by_interviewer(interviewer, requests)
        print(rtv)
        assert rtv == [(datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0))]

    def test_04_get_free_slots(self):
        test_candidate = Candidate('Carl')
        test_candidate.set_requested_slots(self.requests)
        rtv = self.memory_storage.get_free_slots(test_candidate, 'Sarah', 'Philip')
        assert rtv == {(datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                       (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0))}

    def test_05_get_free_slots(self):
        test_candidate = Candidate('Carl')
        test_candidate.set_requested_slots(self.requests)
        rtv = self.memory_storage.get_free_slots(test_candidate, 'Philip')
        assert rtv == {(datetime(2018, 10, 14, 9, 0), datetime(2018, 10, 14, 10, 0)),
                       (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0)),
                       (datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                       (datetime(2018, 10, 16, 11, 0), datetime(2018, 10, 16, 12, 0)),
                       (datetime(2018, 10, 16, 9, 0), datetime(2018, 10, 16, 10, 0)),
                       (datetime(2018, 10, 18, 9, 0), datetime(2018, 10, 18, 10, 0)),
                       (datetime(2018, 10, 16, 10, 0), datetime(2018, 10, 16, 11, 0))}


    def test_06_get_free_slots(self):
        test_candidate = Candidate('Carl')
        test_candidate.set_requested_slots(self.requests)
        rtv = self.memory_storage.get_free_slots(test_candidate, 'Thomas')
        assert rtv == {(datetime(2018, 10, 16, 11, 0), datetime(2018, 10, 16, 12, 0))}


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_01_get_free_slots']
    unittest.main()
