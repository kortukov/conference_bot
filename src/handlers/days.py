import logging


from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

import helpers

MENU, SEARCHING, SENDING, SENDING_DESCRIPTION, SENDING_DESCRIPTION_TIME, SENDING_TIME, DAYS, SECTION, TIME, FEEDBACK, MARKED = range(
    11
)

logger = logging.getLogger(__name__)


def choose_days(update: Update, context: CallbackContext):
    # here goes the code that saves the day
    global event_list
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
    times_list = helpers.create_times_without_food_list(day)

    if context.user_data['by_time']:
        reply_keyboard = []
        if len(times_list) % 2 == 0:
            for i in range(0, len(times_list), 2):
                reply_keyboard.extend([[times_list[i], times_list[i + 1]]])
        else:
            for i in range(0, len(times_list) - 1, 2):
                reply_keyboard.extend([[times_list[i], times_list[i + 1]]])
            reply_keyboard.extend([[times_list[-1]]])

        reply_keyboard.extend(
            [
                [context.user_data['localisation']['BACK']],
                [context.user_data['localisation']['TOBEGINNING']],
            ]
        )

        update.message.reply_text(
            context.user_data['localisation']['CHOOSETIME'],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )
        return TIME
    else:
        reply_keyboard = [
            [context.user_data['localisation']['PLENARY']],
            [context.user_data['localisation']['RESEARCH']],
            [context.user_data['localisation']['WORKSHOPS']],
            [context.user_data['localisation']['FOOD']],
            [context.user_data['localisation']['BACK']],
            [context.user_data['localisation']['TOBEGINNING']],
        ]
        if day == 24:
            reply_keyboard.insert(2, [context.user_data['localisation']['YOUNG']])

        update.message.reply_text(
            context.user_data['localisation']['CHOOSESECTION'],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

        return SECTION


def back_to_days(update: Update, context: CallbackContext):
    reply_keyboard = [
        [context.user_data['localisation']['24']],
        [context.user_data['localisation']['25']],
        [context.user_data['localisation']['TOBEGINNING']],
    ]

    update.message.reply_text(
        context.user_data['localisation']['WHICHDAY'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return DAYS


