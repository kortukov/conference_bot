import pickle


PICKLE_PATH = '../event_list.pickle'
GLOBAL_MARKED_PATH = '../global_marked_list.pickle'


class DataKeeper:
    """This class is used to store all program data (pickle file and path to program).
    It also incapsulates all state constants for ConversationHandler.
    """

    def __init__(self):
        with open(PICKLE_PATH, 'rb') as f:
            self.event_list = pickle.load(f)

        self.global_marked_list = self.load_marked_list()

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

    def load_marked_list(self):
        try:
            f = open(GLOBAL_MARKED_PATH, 'rb')
            global_marked_list = pickle.load(f)
        except Exception:
            global_marked_list = {}
        return global_marked_list

    def save_marked_list(self):
        with open(GLOBAL_MARKED_PATH, 'wb') as f:
            pickle.dump(self.global_marked_list, f, pickle.HIGHEST_PROTOCOL)