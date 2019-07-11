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

    with open('event_list.json', 'r') as f:

        event_list = []
        for line in f:
            event_list.append(jsonpickle.decode(line))

        with open('event_list.pickle', 'wb') as f:
            pickle.dump(event_list, f, pickle.HIGHEST_PROTOCOL)

        print("Pickle complete !")
