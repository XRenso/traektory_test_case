import pytest
from scheduler import Scheduler

TEST_DATA = {
    "days": [
            {"id":1,"date":"2025-02-15","start":"09:00","end":"21:00"},
            {"id":2,"date":"2025-02-16","start":"08:00","end":"22:00"},
            {"id":3,"date":"2025-02-17","start":"09:00","end":"18:00"},
            {"id":4,"date":"2025-02-18","start":"10:00","end":"18:00"},
            {"id":5,"date":"2025-02-19","start":"09:00","end":"18:00"}
    ],
    "timeslots":[
            {"id":1,"day_id":1,"start":"17:30","end":"20:00"},
            {"id":2,"day_id":1,"start":"09:00","end":"12:00"},
            {"id":3,"day_id":2,"start":"14:30","end":"18:00"},
            {"id":4,"day_id":2,"start":"09:30","end":"11:00"},
            {"id":5,"day_id":3,"start":"12:30","end":"18:00"},
            {"id":6,"day_id":4,"start":"10:00","end":"11:00"},
            {"id":7,"day_id":4,"start":"11:30","end":"14:00"},
            {"id":8,"day_id":4,"start":"14:00","end":"16:00"},
            {"id":9,"day_id":4,"start":"17:00","end":"18:00"}
    ]
             }


@pytest.fixture
def scheduler():
    return Scheduler(test_data=TEST_DATA)

@pytest.mark.parametrize("date, expected", [
    ("2025-02-15", [ ("09:00", "12:00"), ("17:30", "20:00")]),
    ("2025-02-19", []),
    ("2025-02-20", []),
])
def test_get_busy_slots(scheduler, date, expected):
    assert scheduler.get_busy_slots(date) == expected

@pytest.mark.parametrize("date, expected", [
    ("2025-02-15", [("12:00", "17:30"), ("20:00", "21:00")]),
    ("2025-02-16", [("08:00", "09:30"), ("11:00", "14:30"), ("18:00", "22:00")]),
    ("2025-02-17", [("09:00", "12:30")]),
    ("2025-02-18", [("11:00", "11:30"), ("16:00", "17:00")]),
    ("2025-02-19", [("09:00", "18:00")]),
])
def test_get_free_slots(scheduler, date, expected):
    assert scheduler.get_free_slots(date) == expected

@pytest.mark.parametrize("date, start, end, expected", [
    ("2025-02-15", "12:00", "13:00", True),
    ("2025-02-15", "10:00", "11:00", False),
    ("2025-02-16", "08:00", "09:00", True),
    ("2025-02-16", "09:30", "10:00", False),
    ("2025-02-18", "11:00", "11:30", True),
    ("2025-02-18", "10:00", "11:00", False),
    ("2025-02-19", "09:00", "15:00", True),

])
def test_is_available(scheduler, date, start, end, expected):
    assert scheduler.is_available(date, start, end) == expected

@pytest.mark.parametrize("duration, expected", [
    (15, ("2025-02-15", "12:00", "12:15")),
    (60, ("2025-02-15", "12:00", "13:00")),
    (90, ("2025-02-15", "12:00", "13:30")),
    (180, ("2025-02-15", "12:00", "15:00")),
    (360, ("2025-02-19", "09:00", "15:00")),
    (480, ("2025-02-19", "09:00", "17:00")),
    (1000, None),

])
def test_find_slot_for_duration(scheduler, duration, expected):
    assert scheduler.find_slot_for_duration(duration) == expected