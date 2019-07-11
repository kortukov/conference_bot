import logging
import pickle

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

from classes import (
    FullEvent,
    Other,
)

import helpers
from . import  main_menu, feedback, search, program, days, program_time, mark_talks


PICKLE_PATH = '../event_list.pickle'

logger = logging.getLogger(__name__)

MENU, SEARCHING, SENDING, SENDING_DESCRIPTION, SENDING_DESCRIPTION_TIME, SENDING_TIME, DAYS, SECTION, TIME, FEEDBACK, MARKED = range(
    11
)


def create_coversation_handler():

    with open(PICKLE_PATH, 'rb') as f:
        event_list = pickle.load(f)

    description_handlers = []
    for event in event_list:
        if isinstance(event, FullEvent) or isinstance(event, Other):
            command = 'desc' + str(event.number)
            description_handlers.append(CommandHandler(command, program.send_description))

    mark_handlers = []
    unmark_handlers = []
    for event in event_list:
        if isinstance(event, FullEvent):
            for talk in event.sublist:
                talk_number = talk[3]
                mark_command = 'mark' + str(talk_number)
                mark_handlers.append(CommandHandler(mark_command, mark_talks.mark_and_unmark_talk))
                unmark_command = 'unmark' + str(talk_number)
                unmark_handlers.append(CommandHandler(unmark_command, mark_talks.mark_and_unmark_talk))

    all_times_regex = helpers.create_all_times_regex()

    return ConversationHandler(
        entry_points=[CommandHandler('start', main_menu.beginning)],
        # It is necessary to write both languages in the regex handlers. No idea how to do it better.
        states={
            MENU: [
                MessageHandler(
                    Filters.regex('^(Показать программу по секциям|Show the conference program)$'),
                    program.show_program,
                ),
                MessageHandler(
                    Filters.regex('^(Показать программу по времени|Show program by time)$'),
                    program_time.show_program_time,
                ),
                MessageHandler(
                    Filters.regex('^(Найти доклад или автора|Find presentation or speaker)$'),
                    search.search_program,
                ),
                MessageHandler(
                    Filters.regex('^(Прислать программу в PDF|Send the program as PDF)$'),
                    main_menu.send_pdf,
                ),
                MessageHandler(Filters.regex('^(English|Русский)$'), main_menu.change_lang),
                MessageHandler(
                    Filters.regex('^(Оставить фидбек|Leave feedback)$'), feedback.leave_feedback
                ),
                MessageHandler(
                    Filters.regex('^(Отмеченные доклады|Marked talks)$'), mark_talks.show_marked_talks
                ),
            ],
            MARKED: [
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning)
            ]
            + mark_handlers
            + unmark_handlers,
            FEEDBACK: [
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
                MessageHandler(Filters.text, feedback.save_feedback),
            ],
            SEARCHING: [
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
                MessageHandler(
                    Filters.regex('^(Ещё результаты|More results)$'), search.search_more
                ),
                MessageHandler(Filters.text, search.perform_search),
            ]
            + description_handlers
            + mark_handlers
            + unmark_handlers,
            SENDING: [
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
                MessageHandler(Filters.regex('^(Назад|Back)$'), program.back_to_sections),
            ]
            + description_handlers,
            SENDING_DESCRIPTION: [
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
                MessageHandler(Filters.regex('^(Назад|Back)$'), program.back_to_message),
            ]
            + mark_handlers
            + unmark_handlers,
            DAYS: [
                MessageHandler(
                    Filters.regex('^(24 сентября|25 сентября|24 September|25 September)$'),
                    days.choose_days,
                ),
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
            ],
            TIME: [
                MessageHandler(Filters.regex(all_times_regex), program_time.choose_time),
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
                MessageHandler(Filters.regex('^(Назад|Back)$'), days.back_to_days),
            ],
            SENDING_TIME: [
                MessageHandler(Filters.regex('^(Назад|Back)$'), program_time.back_to_time),
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
            ]
            + description_handlers,
            SENDING_DESCRIPTION_TIME: [
                MessageHandler(Filters.regex('^(Назад|Back)$'), program_time.back_to_message_time),
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
            ]
            + mark_handlers
            + unmark_handlers,
            SECTION: [
                MessageHandler(
                    Filters.regex('^(Пленарная секция|Plenary session)$'), program.send_data
                ),
                MessageHandler(
                    Filters.regex('(Исследовательская секция|Research Papers Session)$'),
                    program.send_data,
                ),
                MessageHandler(
                    Filters.regex('(Конференция молодых учёных|PhD and student showcase)$'),
                    program.send_data,
                ),
                MessageHandler(
                    Filters.regex(
                        '(Семинары, воркошопы, мастер-классы|Workshops, seminars, master-classes)$'
                    ),
                    program.send_data,
                ),
                MessageHandler(Filters.regex('(Еда|Food)$'), program.send_data),
                MessageHandler(Filters.regex('^(Назад|Back)$'), days.back_to_days),
                MessageHandler(Filters.regex('^(В начало|To beginning)$'), main_menu.beginning),
            ],
        },
        fallbacks=[CommandHandler('quit', quit_conversation), MessageHandler(Filters.text, wrong_message)],
        allow_reentry=True,
        persistent=True,
        name='ConvHandlerName',
    )


def wrong_message(update: Update, context: CallbackContext):
    update.message.reply_text(context.user_data['localisation']['WRONG'])

def quit_conversation(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        context.user_data['localisation']['GOODBYE'], reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

