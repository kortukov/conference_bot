from datetime import datetime
import logging

import telegram
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from classes import FullEvent, Other
import keyboards

logger = logging.getLogger(__name__)

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def show_program(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: show_program", user.first_name, user.last_name, user.username
    )

    reply_keyboard = keyboards.days_keyboard(context)
    context.user_data['by_time'] = False
    update.message.reply_text(
        context.user_data['localisation']['WHICHDAY'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.DAYS


def back_to_sections(update: Update, context: CallbackContext):
    reply_keyboard = keyboards.sections_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['CHOOSESECTION'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.SECTION


def send_data(update: Update, context: CallbackContext):

    day = context.user_data['day']
    message = update.message.text

    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: send_data %s",
        user.first_name,
        user.last_name,
        user.username,
        message,
    )

    reply_message = context.user_data['localisation'][str(day)] + '\n'
    reply_message += message + '\n\n'

    if message == context.user_data['localisation']['PLENARY']:
        types = ['Plenary']
    elif message == context.user_data['localisation']['RESEARCH']:
        types = ['Research']
    elif message == context.user_data['localisation']['YOUNG']:
        types = ['Young']
    elif message == context.user_data['localisation']['WORKSHOPS']:
        types = ['Other', 'Other full events']
    elif message == context.user_data['localisation']['FOOD']:
        types = ['Food']

    reply_keyboard = keyboards.back_to_begin_keyboard(context)

    events = (
        event
        for event in context.user_data['event_list']
        if datetime.fromtimestamp(event.ts_begin).day == day and event.event_type in types
    )
    for result in events:
        if context.user_data['lang'] == 'ru':
            reply_message += (result.str_ru()) + '\n'
        else:
            reply_message += (result.str_en()) + '\n'

        if isinstance(result, FullEvent) or isinstance(result, Other):
            reply_message += (
                context.user_data['localisation']['DETAILS'] + '/desc' + str(result.number) + '\n'
            )


        reply_message += '\n'
    context.user_data['type'] = 'sections'
    context.user_data['message'] = reply_message
    update.message.reply_text(
        reply_message,
        parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return dk.SENDING


def back_to_message(update: Update, context: CallbackContext):
    message_to_send = context.user_data['message']
    reply_keyboard = keyboards.back_to_begin_keyboard(context)
    update.message.reply_text(
        message_to_send,
        parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.SENDING


def send_description(update: Update, context: CallbackContext):
    day = context.user_data['day']
    message = update.message.text
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: send_description %s",
        user.first_name,
        user.last_name,
        user.username,
        message,
    )

    needed_description_number = int(message.split('c')[-1])  # descN
    context.user_data['description_number'] = needed_description_number
    event = next(
        (
            ev
            for ev in context.user_data['event_list']
            if (isinstance(ev, FullEvent) or isinstance(ev, Other))
            and ev.number == needed_description_number
        ),
        None,
    )

    reply_message = context.user_data['localisation'][str(day)] + '\n'
    if context.user_data['lang'] == 'ru':
        reply_message += (event.full_str_ru()) + '\n'
    else:
        reply_message += (event.full_str_en()) + '\n'

    if (
        context.user_data['type'] == 'sections'
        or context.user_data['type'] == 'time'
        or context.user_data['type'] == 'current'
    ):
        reply_keyboard = keyboards.back_to_begin_keyboard(context)
    elif context.user_data['type'] == 'search':
        reply_keyboard = keyboards.to_begin_keyboard(context)

    update.message.reply_text(
        reply_message,
        parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    if context.user_data['type'] == 'sections':
        return dk.SENDING_DESCRIPTION
    elif context.user_data['type'] == 'time':
        return dk.SENDING_DESCRIPTION_TIME
    elif context.user_data['type'] == 'current':
        return dk.SENDING_DESCRIPTION_CURRENT
    elif context.user_data['type'] == 'search':
        update.message.reply_text(context.user_data['localisation']['WHATSEARCH'])
        return dk.SEARCHING
