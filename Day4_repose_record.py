from typing import List, NamedTuple, Tuple
import re
# from collections import namedtuple


# Part 1:

example = '''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up'''.split('\n')

class Record(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    comment: str

class Nap(NamedTuple):
    guard_id: int
    sleep: int
    wake: int


# def collect_entries(lines: List[str]) -> List[Record]:
    
#     regex = '\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.+)'

#     records = []

#     for line in lines:    
#         year, month, day, hour, minute, comment = re.match(regex, line).groups()
#         records.append(Record(int(year), int(month), int(day), int(hour), int(minute), comment))
    
#     return records

def sleepy_time_profiler(entries: List[str]) -> List[Nap]:
    
    entries = sorted(entries)

    naps = [] 

    regex = '\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.+)'
    guard_regex = r"Guard #(\d+) begins shift"
       
    guard_id = sleep = wake = None

    for entry in entries:
        year, month, day, hour, minute, comment = re.match(regex, entry).groups()
        r = Record(int(year), int(month), int(day), int(hour), int(minute), comment)

    # for record in records:
        if ("Guard" in r.comment):
            assert (sleep is None) and (wake is None)
            guard_id = int(re.match(guard_regex, r.comment).groups()[0])

        elif "falls" in r.comment:
            assert (guard_id is not None) and (sleep is None) and (wake is None)
            sleep = r.minute

        elif "wakes" in r.comment:
            assert (guard_id is not None) and (sleep is not None) and (wake is None)
            wake = r.minute
       
        # if (guard_id is not None) and (sleep is not None) and (wake is not None): #!! IMPORTANT !!
            naps.append(Nap(guard_id, sleep, wake))
            sleep = wake = None

    return naps

naps = sleepy_time_profiler(example)

from collections import Counter

def find_sleepiest_guard(naps: List[Nap]) -> int:
    
    c = Counter()

    for nap in naps:
        start = nap.sleep
        end = nap.wake
        c[nap.guard_id] += (end - start)
    
    [(guard_id1, minute1), (guard_id2, minute2)] = c.most_common(2)
    assert minute1 > minute2

    return c.most_common(1)[0][0]

assert find_sleepiest_guard(naps) == 10


def most_asleep_minute(naps: List[Nap], guard_id: int) -> int:

    minute_counter = Counter()

    for nap in naps:

        if (nap.guard_id == guard_id):
            start = nap.sleep
            end = nap.wake

            for minute in range(start, end):
                minute_counter[minute] += 1
            
    [(guard_id1, minute1), (guard_id2, minute2)] = minute_counter.most_common(2)
    assert minute1 > minute2

    return minute_counter.most_common(1)[0][0]

assert most_asleep_minute(naps, 10) == 24

with open('data/day4_input.txt', 'r') as f:
    entries = [line.strip() for line in f]
    naps = sleepy_time_profiler(entries)

sleepiest_guard = find_sleepiest_guard(naps)
sleepiest_minute = most_asleep_minute(naps, sleepiest_guard)

print(sleepiest_guard, sleepiest_minute, sleepiest_guard * sleepiest_minute)


# Part 2:
# list up all the unique guard ids and iterate over them wit List[Nap],
# collect most_common minute and its count value for each id

def most_frequent_minute_by_guard(naps: List[Nap]) -> Tuple[int, int]:
    
    # most_common_minute_by_id_dict = {}
    # id_set = {nap.guard_id for nap in naps}

    # for id_ in id_set:
    minute_counter = Counter()

    for nap in naps:
        # if (nap.guard_id == id_):
        start = nap.sleep
        end = nap.wake

        for minute in range(start, end):
            minute_counter[(nap.guard_id, minute)] += 1

    # most_common_minute_by_id_dict.update({id_: minute_counter.most_common(1)[0]})

    # most_frequent_minute_and_id = sorted(most_common_minute_by_id_dict.items(), key=lambda x: x[1][1], reverse=True)[0] # a tuple
    # most_frequent_id = most_frequent_minute_and_id[0]
    # most_frequent_minute = most_frequent_minute_and_id[1][0]

    [((guard_id1, minute1), count1), ((guard_id2, minute2), count2)] = minute_counter.most_common(2)
    assert count1 > count2

    return (guard_id1, minute1)

# assert most_frequent_minute_by_guard(naps) == (99, 45)

guard_id1, minute1 = most_frequent_minute_by_guard(naps)

print(guard_id1, minute1, guard_id1 * minute1)