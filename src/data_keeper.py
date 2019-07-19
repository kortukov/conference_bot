import pickle


PICKLE_PATH = '../event_list.pickle'
NOTIFICATIONS_PATH = '../notifications.pickle'


class DataKeeper:
    """This class is used to store all program data (pickle file and path to program).
    It also incapsulates all state constants for ConversationHandler.
    """

    def __init__(self):
        with open(PICKLE_PATH, 'rb') as f:
            self.event_list = pickle.load(f)

        try:
            f = open(NOTIFICATIONS_PATH, 'rb')
            self.notifications = pickle.load(f)
        except Exception:
            self.notifications = {}


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

    def save_notifications(self):
        with open(NOTIFICATIONS_PATH, 'wb') as f:
            pickle.dump(self.notifications, f, pickle.HIGHEST_PROTOCOL)