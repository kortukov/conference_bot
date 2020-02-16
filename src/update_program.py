import pickle
import requests
import sys

from data_keeper import DataKeeper
import read_data
from classes import FullEvent
from private_data import TOKEN

PICKLE_PATH = '../event_list.pickle'
DOCX_PATH = '../Program_example.docx'
PERSISTENCE_PATH = 'bot_persistence.pickle'
REQUEST_STRING = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'



def send_update_message(user_id, language):
    print('Placeholder for sending notifications.')
    if language == 'ru':
        message = 'Будьте внимательны: Программа конференции изменилась.'
    else:
        message = 'Attention: The conference program has changed.'

    request_string = REQUEST_STRING.format(token=TOKEN, chat_id=user_id, message=message)
    r = requests.post(request_string)
    print(r)


def get_difference(new_event_list, old_event_list):
    difference = []

    # Sections difference
    for new_event in new_event_list:
        if new_event not in old_event_list:
            difference.append('++++++++' + str(new_event))
    for old_event in old_event_list:
        if old_event not in new_event_list:
            difference.append('--------' + str(old_event))

    # Talks difference
    new_talks = [talk for event in new_event_list for talk in event.talks_list]
    old_talks = [talk for event in old_event_list for talk in event.talks_list]

    for new_talk in new_talks:
        if new_talk not in old_talks:
            difference.append('++++++++' + str(new_talk))
    for old_talk in old_talks:
        if old_talk not in new_talks:
            difference.append('--------' + str(old_talk))
    return difference


if __name__ == '__main__':
    if len(sys.argv) == 2 and (sys.argv[1] == 'print' or sys.argv[1] == 'save_and_send' or sys.argv[1] == 'force'):
        mode = sys.argv[1]
    else:
        sys.exit("Usage: python3 program_update.py print/save_and_send/force\n")

    parser = read_data.ProgramParser()
    new_event_list = parser.parse_program(DOCX_PATH)

    with open(PERSISTENCE_PATH, 'rb') as f:
        persistence = pickle.load(f)

    user_data_dict = persistence['user_data']
    user_ids = list(user_data_dict.keys())

    marks_and_notifications = DataKeeper.load_marks_and_notifications()

    for user_id, user_data in user_data_dict.items():
        user_data.pop('marked_list', None)
        user_data.pop('notified_list', None)

        language = user_data.get('lang', 'ru')
        old_event_list = user_data.get('event_list', [])
        program_difference = get_difference(new_event_list, old_event_list)
        if mode == 'force' or program_difference:
            if mode == 'print':
                for message in program_difference:
                    print(message)
                    print("================")

            else:
                send_update_message(user_id, language)
                user_data['event_list'] = new_event_list

                # recreate marked and notified lists
                user_data['marked_list'] = []
                user_data['notified_list'] = []
                user_marks_and_notifications = marks_and_notifications.get(user_id, [])
                marked_notified_dict = {mn[0]: mn[1] for mn in user_marks_and_notifications}
                for event in new_event_list:
                        for talk in event.talks_list:

                            if talk.title in marked_notified_dict:
                                talk.is_marked = True
                                user_data['marked_list'].append(talk)
                                if marked_notified_dict[talk.title]:
                                    talk.notified = True
                                    user_data['notified_list'].append(talk)

    with open(PERSISTENCE_PATH, 'wb') as f:
        pickle.dump(persistence, f, pickle.HIGHEST_PROTOCOL)
