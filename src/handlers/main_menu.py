import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

import languages
import keyboards


logger = logging.getLogger(__name__)

dk = None


def init_module(data_keeper):
    global dk
    dk = data_keeper


def beginning(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info(
        "Chat_id %s User %s %s username:%s started the conversation.",
        update.message.chat_id,
        user.first_name,
        user.last_name,
        user.username,
    )

    if 'lang' not in context.user_data:
        context.user_data['lang'] = 'ru'
        context.user_data['localisation'] = languages.localisation_ru

    if 'marked_list' not in context.user_data:
        context.user_data['marked_list'] = dk.global_marked_list.get(update.message.chat_id, [])

    if 'notified_list' not in context.user_data:
        context.user_data['notified_list'] = []
        dk.notifications[update.message.chat_id] = []
        dk.save_marked_list()

    if 'event_list' not in context.user_data:
        context.user_data['event_list'] = dk.event_list

    reply_keyboard = keyboards.main_menu_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.MENU


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

    reply_keyboard = keyboards.main_menu_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.MENU


def send_pdf(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s %s username:%s: send_pdf", user.first_name, user.last_name, user.username)

    context.bot.send_document(chat_id=update.message.chat_id, document=open(dk.PROGRAM_PATH, 'rb'))

    reply_keyboard = keyboards.main_menu_keyboard(context)

    update.message.reply_text(
        context.user_data['localisation']['HELLO'],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return dk.MENU
