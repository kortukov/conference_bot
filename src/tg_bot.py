import logging

from telegram import Update
from telegram.ext import Updater, CallbackContext, PicklePersistence

from handlers import conversation, notify
from data_keeper import DataKeeper
from private_data import TOKEN


LOG_PATH = '../log/bot.log'
# deploy logging configs
# logging.basicConfig(
#    filename=LOG_PATH,
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#    level=logging.INFO
# )
# debug logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    data_keeper = DataKeeper()

    my_persistence = PicklePersistence(filename='bot_persistence.pickle')

    updater = Updater(
        token=TOKEN, persistence=my_persistence, use_context=True
    )
    dispatcher = updater.dispatcher

    job_queue = updater.job_queue

    execute_notifications_job = job_queue.run_repeating(
        notify.execute_notifications, interval=55, first=1
    )

    conv_handler = conversation.create_coversation_handler(data_keeper)

    dispatcher.add_handler(conv_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
