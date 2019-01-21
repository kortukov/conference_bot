import pickle
import json
import jsonpickle
from classes import BaseEvent, SimpleEvent, FullEvent, Food, Other, Plenary, Research, Young, OtherFull


if __name__ == '__main__':
	with open('event_list.pickle', 'rb') as f:
		event_list = pickle.load(f)

	'''for ev in event_list:
		print(ev)
		print("=========")'''
	
	with open('event_list.json', 'r') as f:

		for line in f:
			obj_str = jsonpickle.decode(line)
			#obj_str = json.loads(line)
			print(jsonpickle.decode(obj_str))
			#obj = jsonpickle.decode(obj_str)
		obj = []
		for ev in obj:
			print(ev)
			print('========')

