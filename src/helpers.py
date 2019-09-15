from datetime import datetime

from read_data import get_timestamp


dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def create_times_without_food_list(day):
    times_list = create_times_list(day)
    new_times_list = []
    for time_bounds in times_list:
        begin = time_bounds.split('-')[0]
        end = time_bounds.split('-')[1]

        ts_begin = get_timestamp(day, int(begin.split(':')[0]), int(begin.split(':')[1]))
        ts_end = get_timestamp(day, int(end.split(':')[0]), int(end.split(':')[1]))
        events = [
            event
            for event in dk.event_list
            if datetime.fromtimestamp(event.ts_begin).day == day
            and ts_begin == event.ts_begin
            or ts_end == event.ts_end
        ]
        if len(events) == 1:
            if events[0].event_type == 'Food':
                continue
        new_times_list.append(time_bounds)
    new_times_list = sorted(new_times_list, key=lambda x: int(x.split(':')[0]))
    return new_times_list


def create_times_list(day):
    ts_list = [
        [event.ts_begin, event.ts_end]
        for event in dk.event_list
        if datetime.fromtimestamp(event.ts_begin).day == day
    ]
    for i in range(len(ts_list)):
        for j in range(len(ts_list)):
            if ts_list[i][0] == ts_list[j][0]:
                ts_list[i][1] = min(ts_list[i][1], ts_list[j][1])
            elif ts_list[i][1] == ts_list[j][1]:
                ts_list[i][0] = max(ts_list[i][0], ts_list[j][0])

    times_list = [
        str(datetime.fromtimestamp(ts[0]).hour)
        + ':'
        + str(datetime.fromtimestamp(ts[0]).minute)
        + '-'
        + str(datetime.fromtimestamp(ts[1]).hour)
        + ':'
        + str(datetime.fromtimestamp(ts[1]).minute)
        for ts in ts_list
    ]
    times_list = list(set(times_list))

    fixed_times_list = []
    for time in times_list:
        if ':0' in time:
            time = time.replace(':0', ':00')
        fixed_times_list.append(time)
    times_list = fixed_times_list
    times_list.sort()
    first = times_list.pop()
    times_list.insert(0, first)
    return times_list


def create_all_times_regex():
    all_times = []
    for day in range(23, 25):
        times_list = create_times_list(day)
        all_times.extend(times_list)
    all_times = list(set(all_times))
    all_times.sort()
    all_times_regex = '^('
    for time in all_times:
        all_times_regex += time + '|'
    all_times_regex += ')$'
    return all_times_regex
