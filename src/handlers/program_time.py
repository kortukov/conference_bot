from datetime import datetime
import logging

import telegram
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from classes import FullEvent, Other
import keyboards
from read_data import get_timestamp


logger = logging.getLogger(__name__)

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def show_program_time(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: show_program_time", user.first_name, user.last_name, user.username
    )
    reply_keyboard = keyboards.days_keyboard(context)
    context.user_data['by_time'] = True
    update.message.reply_text(
        context.user_data['localisation']['WHICHDAY'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.DAYS


def back_to_time(update: Update, context: CallbackContext):
    reply_keyboard = keyboards.times_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['CHOOSETIME'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.TIME


def choose_time(update: Update, context: CallbackContext):
    day = context.user_data['day']
    time_bounds = update.message.text
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: choose_time %s %s",
        user.first_name,
        user.last_name,
        user.username,
        day,
        time_bounds,
    )

    begin = time_bounds.split('-')[0]
    end = time_bounds.split('-')[1]

    ts_begin = get_timestamp(day, int(begin.split(':')[0]), int(begin.split(':')[1]))
    ts_end = get_timestamp(day, int(end.split(':')[0]), int(end.split(':')[1]))

    # Здесь уже пора выдавать данные
    events = (
        event
        for event in context.user_data['event_list']
        if datetime.fromtimestamp(event.ts_begin).day == day
        and ts_begin == event.ts_begin
        or ts_end == event.ts_end
    )
    reply_message = context.user_data['localisation'][str(day)] + '\n'

    reply_message += time_bounds + '\n\n'

    for result in events:
        reply_message += (result.str_ru()) + '\n'

        if isinstance(result, FullEvent):
            reply_message += (
                context.user_data['localisation']['DETAILS'] + '/desc' + str(result.number) + '\n'
            )
            context.user_data['type'] = 'time'

        reply_message += '\n'

    context.user_data['message'] = reply_message

    reply_keyboard = keyboards.back_to_begin_keyboard(context)

    update.message.reply_text(
        reply_message,
        parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.SENDING_TIME


def back_to_message_time(update: Update, context: CallbackContext):
    message_to_send = context.user_data['message']
    reply_keyboard = keyboards.back_to_begin_keyboard(context)
    update.message.reply_text(
        message_to_send,
        parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.SENDING_TIME
