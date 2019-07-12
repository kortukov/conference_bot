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


def mark_and_unmark_talk(update: Update, context: CallbackContext):
    day = context.user_data['day']
    message = update.message.text
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: mark_talk %s",
        user.first_name,
        user.last_name,
        user.username,
        message,
    )

    needed_number = int(message.split('k')[-1])  # markN
    for event in dk.event_list:
        if isinstance(event, FullEvent):
            for talk in event.sublist:
                if needed_number == talk[3]:
                    if talk[4] == False:
                        talk[4] = True

                        talk_index = event.sublist.index(talk)
                        if context.user_data['lang'] == 'ru':
                            context.user_data['marked_list'].append(
                                context.user_data['localisation'][str(event.get_date())]
                                + '\n'
                                + event.one_talk_str_ru(talk_index)
                            )
                        else:
                            context.user_data['marked_list'].append(
                                context.user_data['localisation'][str(event.get_date())]
                                + '\n'
                                + event.one_talk_str_en(talk_index)
                            )
                    else:
                        talk[4] = False
                        for i in range(len(context.user_data['marked_list'])):
                            if "mark" + str(needed_number) in context.user_data['marked_list'][i]:
                                del context.user_data['marked_list'][i]
                                break

    # Sending previous message again, but updated
    if context.user_data['type'] == 'sections' or context.user_data['type'] == 'time':
        needed_description_number = context.user_data['description_number']
        event = next(
            (
                ev
                for ev in dk.event_list
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
        reply_keyboard = keyboards.back_to_begin_keyboard(context)

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

    elif context.user_data['type'] == 'search':
        reply_messages = context.user_data['search_reply_messages']
        # update the needed message
        for i in range(len(reply_messages)):
            if "mark" + str(needed_number) in reply_messages[i]:
                reply_messages[i] = context.user_data['marked_list'][-1]

        reply_keyboard = keyboards.to_begin_keyboard(context)

        for reply_message in reply_messages:
            update.message.reply_text(
                reply_message,
                parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, resize_keyboard=True
                ),
            )

        return dk.SEARCHING

    elif context.user_data['type'] == 'marked':
        marked_list = context.user_data['marked_list']
        reply_keyboard = keyboards.to_begin_keyboard(context)
        for reply_message in marked_list:
            update.message.reply_text(
                reply_message,
                parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, resize_keyboard=True
                ),
            )

        return dk.MARKED


def show_marked_talks(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: show_marked_talks", user.first_name, user.last_name, user.username
    )
    context.user_data['type'] = 'marked'

    marked_list = context.user_data['marked_list']

    reply_keyboard = keyboards.to_begin_keyboard(context)
    for reply_message in marked_list:
        update.message.reply_text(
            reply_message,
            parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

    return dk.MARKED