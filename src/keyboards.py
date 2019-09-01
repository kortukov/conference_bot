from telegram.ext import CallbackContext

import helpers


def main_menu_keyboard(context: CallbackContext):
    keyboard = [
        [context.user_data['localisation']['SHOWPROGRAM']],
        [context.user_data['localisation']['SHOWPROGRAMTIME']],
        [context.user_data['localisation']['SEARCHPROGRAM']],
        [context.user_data['localisation']['CURRENT']],
        [context.user_data['localisation']['SENDPROGRAM'], context.user_data['localisation']['FEEDBACK']],
        [context.user_data['localisation']['LANGUAGE']],
    ]

    if len(context.user_data['marked_list']) != 0:
        keyboard.insert(3,[context.user_data['localisation']['MARKED']])

    return keyboard


def to_begin_keyboard(context: CallbackContext):
    return [[context.user_data['localisation']['TOBEGINNING']]]


def back_to_begin_keyboard(context: CallbackContext):
    return [
        [context.user_data['localisation']['BACK']],
        [context.user_data['localisation']['TOBEGINNING']],
    ]


def more_to_begin_keyboard(context: CallbackContext):
    return [
        [context.user_data['localisation']['MORE']],
        [context.user_data['localisation']['TOBEGINNING']],
    ]


def more_back_to_begin_keyboard(context: CallbackContext):
    return [
        [context.user_data['localisation']['MORE']],
        [context.user_data['localisation']['BACK']],
        [context.user_data['localisation']['TOBEGINNING']],
    ]



def days_keyboard(context: CallbackContext):
    keyboard = [
        [context.user_data['localisation']['24']],
        [context.user_data['localisation']['25']],
        [context.user_data['localisation']['TOBEGINNING']],
    ]
    return keyboard


def sections_keyboard(context: CallbackContext):
    # here goes the code that saves the day
    day = context.user_data['day']
    keyboard = [
        [context.user_data['localisation']['PLENARY']],
        [context.user_data['localisation']['RESEARCH']],
        [context.user_data['localisation']['WORKSHOPS']],
        [context.user_data['localisation']['FOOD']],
        [context.user_data['localisation']['BACK']],
        [context.user_data['localisation']['TOBEGINNING']],
    ]
    if day == 24:
        keyboard.insert(2, [context.user_data['localisation']['YOUNG']])

    return keyboard


def times_keyboard(context: CallbackContext):
    day = context.user_data['day']
    times_list = helpers.create_times_without_food_list(day)

    keyboard = []
    if len(times_list) % 2 == 0:
        for i in range(0, len(times_list), 2):
            keyboard.extend([[times_list[i], times_list[i + 1]]])
    else:
        for i in range(0, len(times_list) - 1, 2):
            keyboard.extend([[times_list[i], times_list[i + 1]]])
        keyboard.extend([[times_list[-1]]])

    keyboard.extend(back_to_begin_keyboard(context))

    return keyboard


def conflicts_to_begin_keyboard(context: CallbackContext):
    return [
        [context.user_data['localisation']['CONFLICTS']],
        [context.user_data['localisation']['TOBEGINNING']],
    ]

