import logging
from transliterate import translit

import telegram
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from classes import FullEvent
import keyboards

logger = logging.getLogger(__name__)

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def search_program(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: search_program.", user.first_name, user.last_name, user.username
    )

    reply_keyboard = keyboards.to_begin_keyboard(context)
    update.message.reply_text(
        context.user_data['localisation']['WHATSEARCH'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return dk.SEARCHING


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

    # add transliteration
    message_variants = {message}
    try:
        alt_message = translit(message, 'ru')
        message_variants.add(alt_message)
    except:
        pass

    try:
        alt_message = translit(message, 'ru', reversed=True)
        message_variants.add(alt_message)
    except:
        pass

    logger.info('Searching for {}'.format(message_variants))
    context.user_data['reply_messages'] = []
    reply_keyboard = keyboards.to_begin_keyboard(context)
    reply_messages = []
    for event in context.user_data['event_list']:
        if isinstance(event, FullEvent):
            if any(message in event.full_str_ru().lower() for message in message_variants):
                if any(message in event.str_ru().lower() for message in message_variants):
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
                    for talk in event.talks_list:
                        for part in talk.__dict__.values():
                            if any(message in str(part).lower() for message in message_variants):
                                number = event.talks_list.index(talk)
                                reply = (
                                    context.user_data['localisation'][str(event.get_date())]
                                    + '\n'
                                    + event.one_talk_str_ru(number)
                                )
                                reply_messages.append(reply)
                                break  # needed to give one talk only once
            elif any(message in event.full_str_en().lower() for message in message_variants):
                if any(message in event.str_en().lower() for message in message_variants):
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
                    for talk in event.talks_list:
                        for part in talk.__dict__.values():
                            if any(message in str(part).lower() for message in message_variants):
                                number = event.talks_list.index(talk)
                                reply = (
                                    context.user_data['localisation'][str(event.get_date())]
                                    + '\n'
                                    + event.one_talk_str_en(number)
                                )
                                reply_messages.append(reply)
                                break
        else:
            if any(message in event.str_ru().lower() for message in message_variants):
                reply = (
                    context.user_data['localisation'][str(event.get_date())] + '\n' + event.str_ru()
                )
                reply_messages.append(reply)
            elif any(message in event.str_en().lower() for message in message_variants):
                reply = (
                    context.user_data['localisation'][str(event.get_date())] + '\n' + event.str_en()
                )
                reply_messages.append(reply)

    if len(reply_messages) > 5:
        context.user_data['reply_messages'] = reply_messages[5:]
        reply_keyboard = keyboards.more_to_begin_keyboard(context)
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

    return dk.SEARCHING


def search_more(update: Update, context: CallbackContext):
    reply_messages = context.user_data.get('reply_messages', None)
    reply_keyboard = keyboards.to_begin_keyboard(context)
    if not reply_messages:
        reply_messages = [context.user_data['localisation']['NOTFOUND']]
    else:
        if len(reply_messages) > 5:
            context.user_data['reply_messages'] = reply_messages[5:]
            reply_keyboard = keyboards.more_to_begin_keyboard(context)
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

    # this means that state doesn't change
