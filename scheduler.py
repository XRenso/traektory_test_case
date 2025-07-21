import requests
from datetime import datetime, timedelta


def to_time(s):
    return datetime.strptime(s, "%H:%M").time()

def to_date(date, time_str):
    return datetime.combine(datetime.strptime(date, "%Y-%m-%d"), to_time(time_str))


class Scheduler:
    def __init__(self, url=None, test_data=None):
        if not url:
            self.data = test_data
        else:
            self.data = requests.get(url).json()
        self.days = {d["date"]: d for d in self.data["days"]}
        self.timeslots = self.data["timeslots"]


    def get_busy_slots(self, date):
        day = self.days.get(date)
        if not day:
            return []

        return sorted([
            (time_s["start"], time_s["end"])
            for time_s in self.timeslots
            if time_s["day_id"] == day["id"]
        ])

    def get_free_slots(self,date):
        day = self.days.get(date)
        if not day:
            return []

        work_start = to_date(date, day["start"])
        work_end = to_date(date, day["end"])
        busy_slots = ([
            (to_date(date, start), to_date(date, end))
            for start, end in self.get_busy_slots(date)
        ])

        free = []
        current_time = work_start
        for start, end in busy_slots:
            if current_time < start:
                free.append((current_time.strftime("%H:%M"), start.strftime("%H:%M")))
            current_time = max(current_time, end)

        if current_time < work_end:
            free.append((current_time.strftime("%H:%M"), work_end.strftime("%H:%M")))

        return free

    def is_available(self, date, start_str, end_str):
        start = to_date(date, start_str)
        end = to_date(date, end_str)

        for s,e in self.get_busy_slots(date):
            bs = to_date(date, s)
            be = to_date(date, e)

            if not(end <= bs or start >= be):
                return False

        return True

    def find_slot_for_duration(self, duration_minutes):
        delta = timedelta(minutes=duration_minutes)
        for date in self.days:
            free = self.get_free_slots(date)
            for start,end in free:
                s = to_date(date, start)
                e = to_date(date, end)
                if e-s >= delta:
                    slot_end = (s+delta).strftime("%H:%M")
                    return date, s.strftime("%H:%M"), slot_end
        return None


