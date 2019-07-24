import logging
from datetime import datetime

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
    for event in context.user_data['event_list']:
        if isinstance(event, FullEvent):
            for talk in event.talks_list:
                if needed_number == talk.talk_number:
                    if not talk.is_marked:
                        talk.is_marked = True
                        context.user_data['marked_list'].append(talk)
                    else:
                        talk_to_unmark = next(
                            (
                                talk
                                for talk in context.user_data['marked_list']
                                if talk.talk_number == needed_number
                            ),
                            None,
                        )
                        if talk_to_unmark:
                            context.user_data['marked_list'].remove(talk_to_unmark)
                            talk_to_unmark.is_marked = False

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

                    dk.notifications[update.message.chat_id] = context.user_data['notified_list']
                    dk.save_notifications()

    # Sending previous message again, but updated
    if context.user_data['type'] == 'sections' or context.user_data['type'] == 'time':
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
                    reply_messages[i] = context.user_data['marked_list'][-1].str_en()

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
        if find_time_intersections(context):
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

        return dk.MARKED


def show_marked_talks(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: show_marked_talks", user.first_name, user.last_name, user.username
    )
    context.user_data['type'] = 'marked'

    marked_list = context.user_data['marked_list']
    if find_time_intersections(context):
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

    return dk.MARKED


def back_to_marked(update: Update, context: CallbackContext):
    marked_list = context.user_data['marked_list']
    if find_time_intersections(context):
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

    return dk.MARKED


def show_intersections(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: show_intersections", user.first_name, user.last_name, user.username
    )
    reply_keyboard = keyboards.back_to_begin_keyboard(context)

    intersection_list = find_time_intersections(context)
    intersection_list.insert(0, context.user_data['localisation']['CONFLICTMESSAGE'])

    if len(intersection_list) > 5:
        context.user_data['intersection_list'] = intersection_list[5:]
        reply_keyboard = keyboards.more_back_to_begin_keyboard(context)
        intersection_list = intersection_list[:5]

    for intersection in intersection_list:
        update.message.reply_text(
            intersection,
            parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

    return dk.INTERSECTIONS


def show_more_intersections(update: Update, context: CallbackContext):
    intersection_list = context.user_data.get('intersection_list', None)
    logger.critical(context.user_data['intersection_list'])
    reply_keyboard = keyboards.back_to_begin_keyboard(context)
    if not intersection_list:
        intersection_list = [context.user_data['localisation']['NOTFOUND']]
    else:
        if len(intersection_list) > 5:
            context.user_data['intersection_list'] = intersection_list[5:]
            reply_keyboard = keyboards.more_back_to_begin_keyboard(context)
            intersection_list = intersection_list[:5]
        else:
            context.user_data['intersection_list'] = []

    for intersection in intersection_list:
        update.message.reply_text(
            intersection,
            parse_mode=telegram.ParseMode.HTML,  # this is needed for bold text
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )


def find_time_intersections(context: CallbackContext):
    talks_list = context.user_data['marked_list']

    # create time points
    ts_list = []
    for talk in talks_list:
        ts_list.append(talk.ts_begin)
        ts_list.append(talk.ts_end)

    marked_begin = min(ts_list)
    marked_end = max(ts_list)

    time_points = [marked_begin]
    # 600 sec = 10 min
    point = marked_begin + 600
    while point < marked_end:
        time_points.append(point)
        point += 600
    time_points.append(marked_end)

    # create list of intersecting talks in every timepoint
    timepoint_list = []
    talks_already_accounted = set()
    for i in range(len(time_points)):
        point = time_points[i]

        talks_at_this_point = [
            talk for talk in talks_list if talk_at_this_time(talk, point)
        ]

        if len(talks_at_this_point) <= 1:
            continue

        # are there any new talks at this point ?
        if all(talk in talks_already_accounted for talk in talks_at_this_point):
            continue

        [talks_already_accounted.add(talk) for talk in talks_at_this_point]

        timepoint_list.append(talks_at_this_point)

    if context.user_data['lang'] == 'ru':
        intersection_global_list = [
            ''.join(talk.intersect_str(eng=False) for talk in intersections)
            for intersections in timepoint_list
        ]
    else:
        intersection_global_list = [
            ''.join(talk.intersect_str(eng=False) for talk in intersections)
            for intersections in timepoint_list
        ]

    return intersection_global_list


def check_talks_for_intersection(talk_1, talk_2):
    if talk_1.ts_begin < talk_2.ts_begin:
        if talk_1.ts_end <= talk_2.ts_begin:
            return False
        else:
            return True
    else:
        if talk_1.ts_begin >= talk_2.ts_end:
            return False
        else:
            return True


def check_for_intersections_with_times(talk, ts1, ts2):
    if talk.ts_begin < ts1:
        if talk.ts_end <= ts1:
            return False
        else:
            return True
    else:
        if talk.ts_begin >= ts2:
            return False
        else:
            return True


def talk_at_this_time(talk, ts):
    if talk.ts_begin <= ts < talk.ts_end:
        return True
    else:
        return False
    