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

    def full_str_ru(self):
        result = super().str_ru() + '\n\n'
        for talk in self.talks_list:
            result = result + "<b>" + talk.title + '</b>\n'
            if talk.authors:
                result = result + "Авторы:\n\t" + talk.authors + '\n'
            if talk.speaker:
                result = result + "Докладчик:\n\t" + talk.speaker + '\n'
            if talk.talk_number:
                if not talk.is_marked:  # marked
                    result = result + 'Отметить доклад: /mark' + str(talk.talk_number) + '\n'
                else:
                    result = result + 'Убрать отметку: /unmark' + str(talk.talk_number) + '\n'
        return result

    def one_talk_str_ru(self, number):
        result = super().str_ru() + '\n\n'
        if number >= len(self.talks_list):
            return ''
        talk = self.talks_list[number]
        result = result + "<b>" + talk.title + '</b>\n'
        if talk.authors:
            result = result + "Авторы:\n\t" + talk.authors + '\n'
        if talk.speaker:
            result = result + "Докладчик:\n\t" + talk.speaker + '\n\n'
        if talk.talk_number:
            if not talk.is_marked:  # marked
                result = result + 'Отметить доклад: /mark' + str(talk.talk_number) + '\n'
            else:
                result = result + 'Убрать отметку: /unmark' + str(talk.talk_number) + '\n'
        return result

    def full_str_en(self):
        result = ""
        result = super().str_en() + '\n\n'
        for talk in self.talks_list:
            result = result + "<b>" + talk.title + '</b>\n'
            if talk.authors:
                result = result + "Authors:\n\t" + talk.authors + '\n'
            if talk.speaker != "":
                result = result + "Speaker:\n\t" + talk.speaker + '\n\n'
            if talk.talk_number:
                if not talk.is_marked:  # marked
                    result = result + 'Mark talk: /mark' + str(talk.talk_number) + '\n'
                else:
                    result = result + 'Remove mark: /unmark' + str(talk.talk_number) + '\n'
        return result

    def one_talk_str_en(self, number):
        result = ""
        result = super().str_en() + '\n\n'
        if number >= len(self.talks_list):
            return ''
        talk = self.talks_list[number]
        result = result + "<b>" + talk.title + '</b>\n'
        if talk.authors:
            result = result + "Authors:\n\t" + talk.authors + '\n'
        if talk.speaker:
            result = result + "Speaker:\n\t" + talk.speaker + '\n\n'
        if talk.talk_number:
            if not talk.is_marked:  # marked
                result = result + 'Mark talk: /mark' + str(talk.talk_number) + '\n'
            else:
                result = result + 'Remove mark: /unmark' + str(talk.talk_number) + '\n'
        return result


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
    def __init__(self, title, authors, speaker, talk_number, is_marked=False):
        self.title = title
        self.authors = authors
        self.speaker = speaker
        self.talk_number = talk_number
        self.is_marked = is_marked
        self.ts_begin = None
        self.ts_end = None
