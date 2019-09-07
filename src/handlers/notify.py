import logging
import time

import telegram
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from classes import FullEvent, Other
import keyboards
from . import mark_talks

logger = logging.getLogger(__name__)

MIN = 60

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def notify_and_unnotify_talk(update: Update, context: CallbackContext):
    message = update.message.text
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: notify_talk %s",
        user.first_name,
        user.last_name,
        user.username,
        message,
    )

    notification_added = False
    title_to_notify = ''

    needed_number = int(message.split('y')[-1])  # notifyN
    for event in context.user_data['event_list']:
        if isinstance(event, FullEvent):
            for talk in event.talks_list:
                if needed_number == talk.talk_number:
                    if not talk.notified:
                        talk.notified = True
                        context.user_data['notified_list'].append(talk)
                        notification_added = True
                        title_to_notify = talk.title
                    else:
                        talk_to_unnotify = next(
                            (
                                talk
                                for talk in context.user_data['notified_list']
                                if talk.talk_number == needed_number
                            ),
                            None,
                        )
                        if talk_to_unnotify:
                            context.user_data['notified_list'].remove(talk_to_unnotify)
                            talk_to_unnotify.notified = False

                    dk.update_marks_and_notifications(
                        update.message.chat_id, context.user_data['marked_list']
                    )

    # Sending previous message again, but updated
    if (
            context.user_data['type'] == 'sections'
            or context.user_data['type'] == 'time'
            or context.user_data['type'] == 'current'
    ):
        day = context.user_data['day']
        needed_description_number = context.user_data['description_number']
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
        reply_keyboard = keyboards.back_to_begin_keyboard(context)

        if notification_added:
            added_message = context.user_data['localisation']['NOTIFICATIONADDED'] + '\n' + title_to_notify
        else:
            added_message = context.user_data['localisation']['NOTIFICATIONREMOVED']

        for message in (reply_message, added_message):
            update.message.reply_text(
                message,
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
        reply_messages = context.user_data['search_reply_messages']
        # update the needed message
        for i in range(len(reply_messages)):
            if "notify" + str(needed_number) in reply_messages[i]:
                needed_talk = next(
                    (
                        talk
                        for event in context.user_data['event_list']
                        if isinstance(event, FullEvent)
                        for talk in event.talks_list
                        if talk.talk_number == needed_number
                    ),
                    None,
                )
                if context.user_data['lang'] == 'ru':
                    reply_messages[i] = needed_talk.str_ru() if needed_talk else ""
                else:
                    reply_messages[i] = needed_talk.str_en() if needed_talk else ""

        # dirty workaround to remove previous messages
        reply_messages = [
            message for message in reply_messages
            if context.user_data['localisation']['NOTIFICATIONADDED'] not in message
            and context.user_data['localisation']['NOTIFICATIONREMOVED'] not in message
        ]

        if notification_added:
            reply_messages.append(context.user_data['localisation']['NOTIFICATIONADDED'] + '\n' + title_to_notify)
        else:
            reply_messages.append(context.user_data['localisation']['NOTIFICATIONREMOVED'])

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
        if mark_talks.find_time_intersections(context):
            reply_keyboard = keyboards.conflicts_to_begin_keyboard(context)
        else:
            reply_keyboard = keyboards.to_begin_keyboard(context)
        for marked_talk in marked_list:
            if context.user_data['lang'] == 'ru':
                reply_message = marked_talk.str_ru()
            else:
                reply_message = marked_talk.str_en()
            update.message.reply_text(
                reply_message,
                parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, resize_keyboard=True
                ),
            )

        if notification_added:
            reply_message = context.user_data['localisation']['NOTIFICATIONADDED'] + '\n' + title_to_notify
        else:
            reply_message = context.user_data['localisation']['NOTIFICATIONREMOVED']

        update.message.reply_text(
            reply_message,
            parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

        return dk.MARKED


def execute_notifications(context: CallbackContext):

    current_moment = time.time()

    for user_id in dk.marks_and_notifications:
        event_list = dk.create_user_event_list(user_id)
        marked_list = dk.create_user_marked_list(user_id, event_list)
        notified_list = dk.create_user_notified_list(user_id, marked_list)

        if notified_list:
            for talk in notified_list:
                talk_ts = talk.ts_begin
                logger.critical(talk_ts - current_moment)
                if 9*MIN <= talk_ts - current_moment <= 10*MIN:
                    message = 'Через 10 минут доклад:\n\n' + talk.str_ru(notification=True)
                    context.bot.send_message(chat_id=user_id, text=message, parse_mode=telegram.ParseMode.HTML)



