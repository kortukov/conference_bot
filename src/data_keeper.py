import pickle

from classes import FullEvent

PICKLE_PATH = '../event_list.pickle'
MARKS_AND_NOTIFICATIONS_PATH = '../global_marked_list.pickle'


class DataKeeper:
    """This class is used to store all program data (pickle file and path to program).
    It also incapsulates all state constants for ConversationHandler.

    self.marks_and_notifications - dict {<user_id>: tuple(Talk.title: str, notification: bool)}
    """

    def __init__(self):
        with open(PICKLE_PATH, 'rb') as f:
            self.event_list = pickle.load(f)

        self.marks_and_notifications = self.load_marks_and_notifications()

        # conversation state constants
        self.MENU = 0
        self.SEARCHING = 1
        self.SENDING = 2
        self.SENDING_DESCRIPTION = 3
        self.SENDING_DESCRIPTION_TIME = 4
        self.SENDING_TIME = 5
        self.DAYS = 6
        self.SECTION = 7
        self.TIME = 8
        self.FEEDBACK = 9
        self.MARKED = 10
        self.INTERSECTIONS = 11

        # paths to data
        self.PROGRAM_PATH = '../program2018.pdf'

    def load_marks_and_notifications(self):
        try:
            f = open(MARKS_AND_NOTIFICATIONS_PATH, 'rb')
            marks_and_notifications = pickle.load(f)
        except Exception:
            marks_and_notifications = {}
        return marks_and_notifications

    def update_marks_and_notifications(self, user_id, list_of_marked_talks):
        new_marks_and_notifications = [(talk.title, talk.notified) for talk in list_of_marked_talks]
        self.marks_and_notifications[user_id] = new_marks_and_notifications
        self.save_marks_and_notifications()

    def save_marks_and_notifications(self):
        with open(MARKS_AND_NOTIFICATIONS_PATH, 'wb') as f:
            pickle.dump(self.marks_and_notifications, f, pickle.HIGHEST_PROTOCOL)

    def create_user_event_list(self, user_id):
        user_event_list = self.event_list
        user_marks_and_notifications = self.marks_and_notifications.get(user_id, [])

        marked_notified_dict = {mn[0]: mn[1] for mn in user_marks_and_notifications}
        for event in user_event_list:
            if isinstance(event, FullEvent):
                for talk in event.talks_list:

                    if talk.title in marked_notified_dict:
                        talk.is_marked = True
                        if marked_notified_dict[talk.title]:
                            talk.notified = True

        return user_event_list
