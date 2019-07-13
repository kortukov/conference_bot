import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

import keyboards

logger = logging.getLogger(__name__)

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def choose_days(update: Update, context: CallbackContext):
    # here goes the code that saves the day
    day = int(update.message.text.split(' ')[0])
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: choose_days %s",
        user.first_name,
        user.last_name,
        user.username,
        day,
    )

    context.user_data['day'] = day

    if context.user_data['by_time']:
        reply_keyboard = keyboards.times_keyboard(context)

        update.message.reply_text(
            context.user_data['localisation']['CHOOSETIME'],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )
        return dk.TIME
    else:
        reply_keyboard = keyboards.sections_keyboard(context)

        update.message.reply_text(
            context.user_data['localisation']['CHOOSESECTION'],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

        return dk.SECTION


def back_to_days(update: Update, context: CallbackContext):
    reply_keyboard = keyboards.days_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['WHICHDAY'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.DAYS


