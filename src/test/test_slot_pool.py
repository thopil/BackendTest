'''
Created on 14 Oct 2018

@author: thomaspilz
'''
import unittest
from storage_factory import StorageFactory
from datetime import datetime


class Test(unittest.TestCase):

    def setUp(self):
        self.slot_pool = StorageFactory('slot_pool').create_storage()
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
                        ]
                    }

        self.requests = [("2018-10-14 09:00:00", "2018-10-14 10:00:00"),
                    ("2018-10-15 09:00:00", "2018-10-15 10:00:00"),
                    ("2018-10-16 09:00:00", "2018-10-16 12:00:00"),
                    ("2018-10-17 09:00:00", "2018-10-17 10:00:00"),
                    ("2018-10-18 09:00:00", "2018-10-18 10:00:00"),]


        self.slot_pool.set_slots(free_slots)


    def tearDown(self):
        pass


    def test_01_get_all_slots(self):
        rtv = self.slot_pool.get_all_slots()
        #for name, slots in rtv:
        #    print(name, slots)

    def test_02__format_time_ranges(self):
        rtv = self.slot_pool._format_time_ranges(self.requests)
        assert rtv == [(datetime(2018, 10, 14, 9, 0), datetime(2018, 10, 14, 10, 0)),
                       (datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                       (datetime(2018, 10, 16, 9, 0), datetime(2018, 10, 16, 12, 0)),
                       (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0)),
                       (datetime(2018, 10, 18, 9, 0), datetime(2018, 10, 18, 10, 0))]

    def test_03_get_free_slots_by_name(self):
        requests = self.slot_pool._format_time_ranges(self.requests)
        rtv = self.slot_pool.get_free_slots_by_name('Sarah', requests)
        print(rtv)
        assert rtv == [(datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0))]

    def test_04_get_free_slots(self):
        rtv = self.slot_pool.get_free_slots(self.requests, 'Sarah', 'Philip')
        assert rtv == {(datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                       (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0))}

    def test_05_get_free_slots(self):
        rtv = self.slot_pool.get_free_slots(self.requests, 'Philip')
        assert rtv == {(datetime(2018, 10, 14, 9, 0), datetime(2018, 10, 14, 10, 0)),
                       (datetime(2018, 10, 15, 9, 0), datetime(2018, 10, 15, 10, 0)),
                       (datetime(2018, 10, 17, 9, 0), datetime(2018, 10, 17, 10, 0)),
                       (datetime(2018, 10, 18, 9, 0), datetime(2018, 10, 18, 10, 0))}


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_01_get_free_slots']
    unittest.main()
