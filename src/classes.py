from datetime import datetime


def get_place(place_id, eng=False):
    if place_id < 0 or place_id > 11:
        return " "
    places = {
        0: "Сокольники",
        1: "Пассаж",
        2: "Ресторан 'Москва'",
        3: "Охотный ряд",
        4: "Крымский вал",
        5: "Воробьёвы горы",
        6: "Арбат",
        7: "Красные ворота",
        8: "Остоженка",
        9: "Чистые пруды",
        10: "Полянка",
        11: "Маросейка",
    }
    places_eng = {
        0: "Sokolniki",
        1: "Passage",
        2: "Restaurant 'Moskva'",
        3: "Okhotny Ryad",
        4: "Krymsky Val",
        5: "Vorobiovy Gory",
        6: "Arbat",
        7: "Krasnye Vorota",
        8: "Ostozhenka",
        9: "Chistye Prudy",
        10: "Polyanka",
        11: "Maroseika",
    }
    if eng:
        return places_eng[place_id]
    else:
        return places[place_id]


class BaseEvent(object):
    def __init__(self, ts_begin, ts_end, place_id, event_type, title_ru, title_en):
        self.ts_begin = ts_begin
        self.ts_end = ts_end
        self.place_id = place_id
        self.event_type = event_type
        self.title_ru = title_ru
        self.title_en = title_en
        self.talks_list = []

    def __str__(self):
        return (
            "Start: "
            + str(datetime.fromtimestamp(self.ts_begin).time())[:-3]
            + "    End: "
            + str(datetime.fromtimestamp(self.ts_end).time())[:-3]
            + "\n"
            + get_place(self.place_id)
            + "\n"
            + str(self.title_ru)
            + " "
            + str(self.title_en)
        )

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        if (
            self.title_ru == other.title_ru
            and self.title_en == other.title_en
            and self.place_id == other.place_id
            and self.ts_begin == other.ts_begin
            and self.ts_end == other.ts_end
        ):
            return True
        else:
            return False

    def str_ru(self):
        return (
            "Время: "
            + str(datetime.fromtimestamp(self.ts_begin).time())[:-3]
            + " - "
            + str(datetime.fromtimestamp(self.ts_end).time())[:-3]
            + "\nЗал: "
            + get_place(self.place_id)
            + "\n"
            + '<b>'
            + str(self.title_ru)
            + '</b>'
        )

    def str_en(self):
        return (
            "Time: "
            + str(datetime.fromtimestamp(self.ts_begin).time())[:-3]
            + " - "
            + str(datetime.fromtimestamp(self.ts_end).time())[:-3]
            + "\nHall: "
            + get_place(self.place_id)
            + "\n"
            + '<b>'
            + str(self.title_en)
            + '</b>'
        )

    def get_date(self):
        return int(datetime.fromtimestamp(self.ts_begin).day)

    def getEventType(self):
        return self.event_type


# Events with no description: Food, Registration, other without description - only a name for them
class SimpleEvent(BaseEvent):
    def __init__(self, ts_begin, ts_end, place_id, event_type, title_ru, title_en):
        super().__init__(ts_begin, ts_end, place_id, event_type, title_ru, title_en)

    def __str__(self):
        return super().__str__()


class Food(SimpleEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
        super().__init__(ts_begin, ts_end, place_id, "Food", title_ru, title_en)


class Other(SimpleEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en, number):
        self.description = None
        self.number = number
        super().__init__(ts_begin, ts_end, place_id, "Other", title_ru, title_en)

    def __str__(self):
        return super().__str__()

    def full_str_ru(self):
        result = ""
        result = super().str_ru() + '\n\n'
        if self.description is not None:
            result += "Описание:\n\t" + self.description
        return result

    def full_str_en(self):
        result = ""
        result = super().str_en() + '\n\n'
        if self.description is not None:
            result += "Description:\n\t" + self.description
        return result


# Events with description: Plenary session, research session, Young researchers, other with description
class FullEvent(BaseEvent):
    # full events have numbers for commands that print full description
    def __init__(self, ts_begin, ts_end, place_id, event_type, title_ru, title_en, number):
        self.talks_list = []  # list of Talk objects
        self.number = number
        super().__init__(ts_begin, ts_end, place_id, event_type, title_ru, title_en)

    def __str__(self):
        return super().__str__()

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        if (
                self.title_ru == other.title_ru
                and self.title_en == other.title_en
                and self.place_id == other.place_id
                and self.ts_begin == other.ts_begin
                and self.ts_end == other.ts_end
        ):
            if len(self.talks_list) != len(other.talks_list):
                return False
            for this_talk, other_talk in zip(self.talks_list, other.talks_list):
                if this_talk != other_talk:
                    return False
            return True
        else:
            return False

    def full_str_ru(self):
        result = super().str_ru() + '\n\n'
        for talk in self.talks_list:
            result = result + talk.str_ru(short=True)
        return result

    def one_talk_str_ru(self, number):
        result = super().str_ru() + '\n\n'
        if number >= len(self.talks_list):
            return ''
        talk = self.talks_list[number]
        return result + talk.str_ru(short=True)

    def full_str_en(self):
        result = super().str_en() + '\n\n'
        for talk in self.talks_list:
            result = result + talk.str_en(short=True)
        return result

    def one_talk_str_en(self, number):
        result = super().str_en() + '\n\n'
        if number >= len(self.talks_list):
            return ''
        talk = self.talks_list[number]
        return result + talk.str_en(short=True)

    def calculate_talk_times(self):
        event_begin = self.ts_begin
        event_end = self.ts_end
        times_diff = event_end - event_begin
        num_of_talks = len(self.talks_list)
        for index, talk in enumerate(self.talks_list):
            talk.ts_begin = event_begin + (index * (times_diff / num_of_talks))
            talk.ts_end = event_begin + ((index + 1) * (times_diff / num_of_talks))


class Plenary(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en, number):
        super().__init__(ts_begin, ts_end, place_id, "Plenary", title_ru, title_en, number)


class Research(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en, number):
        super().__init__(ts_begin, ts_end, place_id, "Research", title_ru, title_en, number)


class Young(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en, number):
        super().__init__(ts_begin, ts_end, place_id, "Young", title_ru, title_en, number)


class OtherFull(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en, number):
        super().__init__(
            ts_begin, ts_end, place_id, "Other full events", title_ru, title_en, number
        )


class Talk:
    def __init__(self, title, authors, speaker, hall, talk_number, is_marked=False, notified=False):
        self.title = title
        self.authors = authors
        self.speaker = speaker
        self._hall = hall
        self.talk_number = talk_number
        self.is_marked = is_marked
        self.notified = notified
        self.ts_begin = None
        self.ts_end = None

    @property
    def hall_ru(self):
        return get_place(self._hall)

    @property
    def hall_en(self):
        return get_place(self._hall, eng=True)

    def __repr__(self):
        return self.str_ru(False, True)

    def __eq__(self, other):
        if (
                self.title == other.title
                and self.authors == other.authors
                and self.speaker == other.speaker
                and self._hall == other._hall
                and self.ts_begin == other.ts_begin
                and self.ts_end == other.ts_end
        ):
            return True
        else:
            return False

    def str_ru(self, short=False, notification=False):
        result = "<b>" + self.title + '</b>\n'
        if self.authors:
            result = result + "Авторы:\n\t" + self.authors + '\n'
        if self.speaker:
            result = result + "Докладчик:\n\t" + self.speaker + '\n'
        if self.ts_begin and self.ts_end:
            result = result + self.get_datetime_ru()
        if self._hall is not None and not short:
            result = result + "Зал: <b>" + self.hall_ru + '</b>\n'

        if notification:
            return result

        if self.talk_number:
            if not self.is_marked:  # marked
                result = result + 'Отметить доклад: /mark' + str(self.talk_number) + '\n'
            else:
                result = result + 'Убрать отметку: /unmark' + str(self.talk_number) + '\n'

                if not self.notified:
                    result = (
                        result + 'Поставить уведомление: /notify' + str(self.talk_number) + '\n'
                    )
                else:
                    result = result + 'Убрать уведомление: /unnotify' + str(self.talk_number) + '\n'

        return result

    def str_en(self, short=False, notification=False):
        result = "<b>" + self.title + '</b>\n'
        if self.authors:
            result = result + "Authors:\n\t" + self.authors + '\n'
        if self.speaker:
            result = result + "Speaker:\n\t" + self.speaker + '\n'
        if self.ts_begin and self.ts_end:
            result = result + self.get_datetime_en()
        if self._hall is not None and not short:
            result = result + "Hall: <b>" + self.hall_en + '</b>\n'

        if notification:
            return result

        if self.talk_number:
            if not self.is_marked:  # marked
                result = result + 'Mark talk: /mark' + str(self.talk_number) + '\n'
            else:
                result = result + 'Remove mark: /unmark' + str(self.talk_number) + '\n'

                if not self.notified:
                    result = result + 'Notify: /notify' + str(self.talk_number) + '\n'
                else:
                    result = (
                        result + 'Remove notification: /unnotify' + str(self.talk_number) + '\n'
                    )

        return result

    def get_datetime_ru(self):
        result = (
            "Время: "
            + str(datetime.fromtimestamp(self.ts_begin).day)
            + ".09 <b>"
            + str(datetime.fromtimestamp(self.ts_begin).time())[:-3]
            + " - "
            + str(datetime.fromtimestamp(self.ts_end).time())[:-3]
            + '</b>\n '
        )
        return result

    def get_datetime_en(self):
        result = (
            "Time: "
            + str(datetime.fromtimestamp(self.ts_begin).day)
            + ".09 <b>"
            + str(datetime.fromtimestamp(self.ts_begin).time())[:-3]
            + " - "
            + str(datetime.fromtimestamp(self.ts_end).time())[:-3]
            + '</b>\n '
        )
        return result

    def intersect_str(self, eng=False):
        if eng:
            return self.get_datetime_en() + self.title + ' <b>' + self.hall_en + '</b>\n----\n'
        else:
            return self.get_datetime_ru() + self.title + ' <b>' + self.hall_ru + '</b>\n----\n'
