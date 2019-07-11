import sys
import pickle
import json
import jsonpickle
from classes import (
    BaseEvent,
    SimpleEvent,
    FullEvent,
    Food,
    Other,
    Plenary,
    Research,
    Young,
    OtherFull,
)


if __name__ == '__main__':

    if len(sys.argv) == 2 and (sys.argv[1] == 'json' or sys.argv[1] == 'pickle'):
        mode = sys.argv[1]
    else:
        sys.exit("Usage: python3 test.py   pickle/json\nNo default.")

    if mode == 'pickle':
        with open('../event_list.pickle', 'rb') as f:
            event_list = pickle.load(f)

        for ev in event_list:
            print(ev)
            print("=========")

    if mode == 'json':
        with open('../event_list.json', 'r') as f:

            event_list = []
            for line in f:
                event_list.append(jsonpickle.decode(line))

            for ev in event_list:
                print(ev)
                print('========')
