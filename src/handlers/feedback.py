import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext



FEEDBACK_PATH = '../log/feedback.log'

logger = logging.getLogger(__name__)
feedback_logger = logging.getLogger('feedback_logger')
f_handler = logging.FileHandler(FEEDBACK_PATH)
feedback_logger.addHandler(f_handler)


MENU, SEARCHING, SENDING, SENDING_DESCRIPTION, SENDING_DESCRIPTION_TIME, SENDING_TIME, DAYS, SECTION, TIME, FEEDBACK, MARKED = range(
    11
)


def leave_feedback(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: leave_feedback", user.first_name, user.last_name, user.username
    )

    reply_keyboard = [[context.user_data['localisation']['TOBEGINNING']]]

    update.message.reply_text(
        context.user_data['localisation']['FEEDBACKMESSAGE'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return FEEDBACK


def save_feedback(update: Update, context: CallbackContext):
    message = update.message.text
    user = update.message.from_user

    feedback_logger.info(
        "User %s %s username:%s: left message:\n%s",
        user.first_name,
        user.last_name,
        user.username,
        message,
    )

    context.bot.send_message(
        chat_id=update.message.chat_id, text=context.user_data['localisation']['FEEDBACKTHANKYOU']
    )
    reply_keyboard = [
        [context.user_data['localisation']['SHOWPROGRAM']],
        [context.user_data['localisation']['SHOWPROGRAMTIME']],
        [context.user_data['localisation']['SEARCHPROGRAM']],
        [context.user_data['localisation']['SENDPROGRAM']],
        [context.user_data['localisation']['LANGUAGE']],
        [context.user_data['localisation']['FEEDBACK']],
    ]

    if len(context.user_data['marked_list']) != 0:
        reply_keyboard.append([context.user_data['localisation']['MARKED']])

    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return MENU