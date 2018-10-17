import numpy as np
from datetime import timedelta, datetime
from functools import reduce

interviewer_data = {
    "Philip": [
        ["2018-10-14 09:00:00", "2018-10-14 16:00:00"],
        ["2018-10-15 09:00:00", "2018-10-15 16:00:00"],
        ["2018-10-16 09:00:00", "2018-10-16 16:00:00"],
        ["2018-10-17 09:00:00", "2018-10-17 16:00:00"],
        ["2018-10-18 09:00:00", "2018-10-18 16:00:00"]
    ],
    "Sarah": [
        ["2018-10-14 12:00:00", "2018-10-14 18:00:00"],
        ["2018-10-15 09:00:00", "2018-10-15 12:00:00"],
        ["2018-10-16 12:00:00", "2018-10-16 18:00:00"],
        ["2018-10-17 09:00:00", "2018-10-17 16:00:00"]
    ],
    #"Thomas": [
    #    ["2018-10-16 11:00:00", "2018-10-16 18:00:00"]
    #]
}

candidate_data = {'Carl': [
        ["2018-10-14 09:00:00", "2018-10-14 10:00:00"],
        ["2018-10-15 09:00:00", "2018-10-15 10:00:00"],
        ["2018-10-16 09:00:00", "2018-10-16 12:00:00"],
        ["2018-10-17 09:00:00", "2018-10-17 10:00:00"],
        ["2018-10-18 09:00:00", "2018-10-18 10:00:00"]
    ]
}

dt_format = '%Y-%m-%d %H:%M:%S'

def create_slots_array(slots):
    slot_array = np.array([])
    for slot in slots:
        begin_str, end_str = slot
        begin = datetime.strptime(begin_str, dt_format)
        end   = datetime.strptime(end_str, dt_format)
        arr = np.array([begin + timedelta(hours=i) for i in range(end.hour-begin.hour)])
        slot_array = np.concatenate((slot_array, arr))
    return slot_array

def create_np_container(input_data):
    container = {}
    for name, slots in input_data.items():
        container[name] = create_slots_array(slots)
    return container

interviewer = create_np_container(interviewer_data)
candidates = create_np_container(candidate_data)

interviewer_slots = [interviewer.get(name) for name in interviewer]
candidate_slots =   [candidates.get(name) for name in candidates]
slots = interviewer_slots + candidate_slots

result = reduce(np.intersect1d, slots)
print(result)
