import logging
import pickle

import telegram
from telegram import ReplyKeyboardMarkup,  Update
from telegram.ext import CallbackContext

from classes import FullEvent


PICKLE_PATH = '../event_list.pickle'

logger = logging.getLogger(__name__)

MENU, SEARCHING, SENDING, SENDING_DESCRIPTION, SENDING_DESCRIPTION_TIME, SENDING_TIME, DAYS, SECTION, TIME, FEEDBACK, MARKED = range(
    11
)
event_list = []
with open(PICKLE_PATH, 'rb') as f:
    event_list = pickle.load(f)


def search_program(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: search_program.", user.first_name, user.last_name, user.username
    )

    reply_keyboard = [[context.user_data['localisation']['TOBEGINNING']]]
    update.message.reply_text(
        context.user_data['localisation']['WHATSEARCH'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return SEARCHING


def perform_search(update: Update, context: CallbackContext):
    message = update.message.text.lower()
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: search: %s",
        user.first_name,
        user.last_name,
        user.username,
        message,
    )

    context.user_data['reply_messages'] = []
    reply_keyboard = [[context.user_data['localisation']['TOBEGINNING']]]
    reply_messages = []
    for event in event_list:
        if isinstance(event, FullEvent):
            if message in event.full_str_ru().lower():
                if message in event.str_ru().lower():
                    reply = (
                        context.user_data['localisation'][str(event.get_date())]
                        + '\n'
                        + event.str_ru()
                        + '\n'
                    )
                    reply += (
                        context.user_data['localisation']['DETAILS']
                        + '/desc'
                        + str(event.number)
                        + '\n'
                    )
                    context.user_data['day'] = event.get_date()
                    reply_messages.append(reply)
                else:
                    for talk in event.sublist:
                        for part in talk:
                            if message in str(part).lower():
                                number = event.sublist.index(talk)
                                reply = (
                                    context.user_data['localisation'][str(event.get_date())]
                                    + '\n'
                                    + event.one_talk_str_ru(number)
                                )
                                reply_messages.append(reply)
                                break  # needed to give one talk only once
            elif message in event.full_str_en().lower():
                if message in event.str_en().lower():
                    reply = (
                        context.user_data['localisation'][str(event.get_date())]
                        + '\n'
                        + event.str_en()
                        + '\n'
                    )
                    reply += (
                        context.user_data['localisation']['DETAILS']
                        + '/desc'
                        + str(event.number)
                        + '\n'
                    )
                    context.user_data['day'] = event.get_date()
                    reply_messages.append(reply)
                else:
                    for talk in event.sublist:
                        for part in talk:
                            if message in str(part).lower():
                                number = event.sublist.index(talk)
                                reply = (
                                    context.user_data['localisation'][str(event.get_date())]
                                    + '\n'
                                    + event.one_talk_str_en(number)
                                )
                                reply_messages.append(reply)
                                break
        else:
            if message in event.str_ru().lower():
                reply = (
                    context.user_data['localisation'][str(event.get_date())] + '\n' + event.str_ru()
                )
                reply_messages.append(reply)
            elif message in event.str_en().lower():
                reply = (
                    context.user_data['localisation'][str(event.get_date())] + '\n' + event.str_en()
                )
                reply_messages.append(reply)

    if len(reply_messages) > 5:
        context.user_data['reply_messages'] = reply_messages[5:]
        reply_keyboard = [
            [context.user_data['localisation']['MORE']],
            [context.user_data['localisation']['TOBEGINNING']],
        ]
        reply_messages = reply_messages[:5]

    if len(reply_messages) == 0:
        reply_messages.append(context.user_data['localisation']['NOTFOUND'])

    reply_messages.append(context.user_data['localisation']['WHATSEARCH'])
    # save messages for mark_and_unmark_talk function
    context.user_data['search_reply_messages'] = reply_messages
    context.user_data['type'] = 'search'
    for reply_message in reply_messages:
        update.message.reply_text(
            reply_message,
            parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

    return SEARCHING


def search_more(update: Update, context: CallbackContext):
    reply_messages = context.user_data.get('reply_messages', None)
    reply_keyboard = [[context.user_data['localisation']['TOBEGINNING']]]
    if reply_messages == None or reply_messages == []:
        reply_messages = [context.user_data['localisation']['NOTFOUND']]
    else:
        if len(reply_messages) > 5:
            context.user_data['reply_messages'] = reply_messages[5:]
            reply_keyboard = [
                [context.user_data['localisation']['MORE']],
                [context.user_data['localisation']['TOBEGINNING']],
            ]
            reply_messages = reply_messages[:5]
        else:
            context.user_data['reply_messages'] = []

    for reply_message in reply_messages:
        update.message.reply_text(
            reply_message,
            parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )
