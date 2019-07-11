import logging

from telegram import  ReplyKeyboardMarkup,  Update
from telegram.ext import CallbackContext

import languages

logger = logging.getLogger(__name__)

PROGRAM_PATH = '../program2018.pdf'

MENU, SEARCHING, SENDING, SENDING_DESCRIPTION, SENDING_DESCRIPTION_TIME, SENDING_TIME, DAYS, SECTION, TIME, FEEDBACK, MARKED = range(
    11
)


def beginning(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s started the conversation.",
        user.first_name,
        user.last_name,
        user.username,
    )

    if 'lang' not in context.user_data:
        context.user_data['lang'] = 'ru'
        context.user_data['localisation'] = languages.localisation_ru

    if 'marked_list' not in context.user_data:
        context.user_data['marked_list'] = []

    reply_keyboard = [
        [context.user_data['localisation']['SHOWPROGRAM']],
        [context.user_data['localisation']['SHOWPROGRAMTIME']],
        [context.user_data['localisation']['SEARCHPROGRAM']],
        [context.user_data['localisation']['SENDPROGRAM']],
        [context.user_data['localisation']['LANGUAGE']],
        [context.user_data['localisation']['FEEDBACK']],
    ]

    if len(context.user_data['marked_list']) != 0:
        reply_keyboard.append([context.user_data['localisation']['MARKED']])

    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return MENU


def change_lang(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "User %s %s username:%s: change_lang to %s",
        user.first_name,
        user.last_name,
        user.username,
        context.user_data['localisation']['LANGUAGE'],
    )

    if context.user_data['lang'] == 'ru':
        context.user_data['localisation'] = languages.localisation_en
        context.user_data['lang'] = 'en'
    else:
        context.user_data['localisation'] = languages.localisation_ru
        context.user_data['lang'] = 'ru'

    reply_keyboard = [
        [context.user_data['localisation']['SHOWPROGRAM']],
        [context.user_data['localisation']['SHOWPROGRAMTIME']],
        [context.user_data['localisation']['SEARCHPROGRAM']],
        [context.user_data['localisation']['SENDPROGRAM']],
        [context.user_data['localisation']['LANGUAGE']],
        [context.user_data['localisation']['FEEDBACK']],
    ]

    if len(context.user_data['marked_list']) != 0:
        reply_keyboard.append([context.user_data['localisation']['MARKED']])

    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return MENU


def send_pdf(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s %s username:%s: send_pdf", user.first_name, user.last_name, user.username)

    context.bot.send_document(chat_id=update.message.chat_id, document=open(PROGRAM_PATH, 'rb'))
    reply_keyboard = [
        [context.user_data['localisation']['SHOWPROGRAM']],
        [context.user_data['localisation']['SHOWPROGRAMTIME']],
        [context.user_data['localisation']['SEARCHPROGRAM']],
        [context.user_data['localisation']['SENDPROGRAM']],
        [context.user_data['localisation']['LANGUAGE']],
        [context.user_data['localisation']['FEEDBACK']],
    ]
    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return MENU

