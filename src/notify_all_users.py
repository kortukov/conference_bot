import pickle
import requests
import sys
from private_data import TOKEN

PERSISTENCE_PATH = 'bot_persistence.pickle'

REQUEST_STRING = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'


def send_message_to_user(user_id, message):
    request_string = REQUEST_STRING.format(token=TOKEN, chat_id=user_id, message=message)
    r = requests.post(request_string)
    print(r)


def query_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def get_bot_user_ids_list(persistence_path):
    with open(persistence_path, 'rb') as f:
        persistence = pickle.load(f)

    user_data_dict = persistence['user_data']
    user_ids = list(user_data_dict.keys())
    return user_ids


if __name__ == '__main__':
    bot_user_ids_list = get_bot_user_ids_list(PERSISTENCE_PATH)
    if not bot_user_ids_list:
        sys.stdout.write('В persistence файле нет пользователей бота.')
        exit()
    sys.stdout.write('Введите сообщение, которое вы хотите отправить всем пользователям бота:\n')
    message = input()
    question = 'Вы уверены, что хотите отправить сообщение\n "{}" ?'.format(message)
    if query_yes_no(question):
        for user_id in bot_user_ids_list:
            send_message_to_user(user_id, message)
    else:
        sys.stdout.write('Нет так нет\n')
