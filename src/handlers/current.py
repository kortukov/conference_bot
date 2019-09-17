import logging
import time

import telegram
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

import languages
import keyboards
from classes import FullEvent, Other

logger = logging.getLogger(__name__)

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def show_current(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: show_current", user.first_name, user.last_name, user.username
    )
    current_moment = time.time()
    #current_moment = 1569240000  # 23.09.19 15:00
    day = 23
    current_sections_messages = []
    for event in context.user_data['event_list']:
        if event.ts_begin <= current_moment <= event.ts_end:
            # found current event
            day = event.get_date()
            if context.user_data['lang'] == 'ru':
                event_message = event.str_ru() + '\n'
            else:
                event_message = event.str_en() + '\n'

            if isinstance(event, FullEvent) or isinstance(event, Other):
                event_message += (
                    context.user_data['localisation']['DETAILS']
                    + '/desc'
                    + str(event.number)
                    + '\n'
                )
            current_sections_messages.append(event_message)
    context.user_data['day'] = day

    if not current_sections_messages:
        current_sections_messages.append(context.user_data['localisation']['NOCURRENT'])

    reply_keyboard = keyboards.to_begin_keyboard(context)

    for message in current_sections_messages:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=message,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

    context.user_data['type'] = 'current'
    context.user_data['messages'] = current_sections_messages

    return dk.SENDING_CURRENT


def back_to_message_current(update: Update, context: CallbackContext):
    messages_to_send = context.user_data['messages']
    reply_keyboard = keyboards.to_begin_keyboard(context)
    for message in messages_to_send:
        update.message.reply_text(
            message,
            parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

    return dk.SENDING_CURRENT
