import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

import keyboards

FEEDBACK_PATH = '../log/feedback.log'

logger = logging.getLogger(__name__)
feedback_logger = logging.getLogger('feedback_logger')
f_handler = logging.FileHandler(FEEDBACK_PATH)
feedback_logger.addHandler(f_handler)

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def leave_feedback(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: leave_feedback", user.first_name, user.last_name, user.username
    )

    reply_keyboard = keyboards.to_begin_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['FEEDBACKMESSAGE'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.FEEDBACK


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
    reply_keyboard = keyboards.main_menu_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.MENU
