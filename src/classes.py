from datetime import datetime

def get_place(place_id, eng = False):
    if place_id < 0 or place_id > 11: return " "
    places = {
    0 : "Сокольники",
    1 : "Пассаж",
    2 : "Ресторан 'Москва'",
    3 : "Охотный ряд",
    4 : "Крымский вал",
    5 : "Воробьёвы горы",
    6 : "Арбат",
    7 : "Красные ворота",
    8 : "Остоженка",
    9 : "Чистые пруды",
    10: "Полянка",
    11: "Маросейка"
    } 
    places_eng = {
        0 : "Sokolniki",
        1 : "Passage",
        2 : "Restaurant 'Moskva'",
        3 : "Okhotny Ryad",
        4 : "Krymsky Val",
        5 : "Vorobiovy Gory", 
        6 : "Arbat",
        7 : "Krasnye Vorota",
        8 : "Ostozhenka",
        9 : "Chistye Prudy",
        10: "Polyanka",
        11: "Maroseika"
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
        return "Start: " + str(datetime.fromtimestamp(self.ts_begin).time())[:-3] + "    End: " + str(datetime.fromtimestamp(self.ts_end).time())[:-3] + "\n" + get_place(self.place_id) + "\n" + str(self.title_ru) + " " + str(self.title_en)
    
    def str_ru(self):
        return "Начало: " + str(datetime.fromtimestamp(self.ts_begin).time())[:-3] + \
        "    Конец: " + str(datetime.fromtimestamp(self.ts_end).time())[:-3] + \
        "\nЗал: " + get_place(self.place_id) + "\n" + \
        '<b>' + str(self.title_ru) + '</b>'

    def str_en(self):
        return "Start: " + str(datetime.fromtimestamp(self.ts_begin).time())[:-3] + \
        "    End: " + str(datetime.fromtimestamp(self.ts_end).time())[:-3] + \
        "\nHall: " + get_place(self.place_id, eng = True) + "\n" + \
        '<b>' + str(self.title_en) + '</b>'


    def getEventType(self):
        return self.event_type

#Events with no description: Food, Registration, other without description - only a name for them
class SimpleEvent(BaseEvent):
    def __init__(self, ts_begin, ts_end, place_id, event_type, title_ru, title_en):
        super().__init__(ts_begin, ts_end, place_id, event_type, title_ru, title_en)
    def __str__(self):
        return super().__str__()

class Food(SimpleEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin, ts_end, place_id, "Food", title_ru, title_en)

class Other(SimpleEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
        self. description = None
        super().__init__(ts_begin, ts_end, place_id, "Other", title_ru, title_en)

    def __str__(self):
        return super().__str__()

    def full_str(self):
        result = ""
        result = super().__str__() + '\n' 
        if self.description != None:
            result += "Description:\n\t" + self.description
        return result

#Events with description: Plenary session, research session, Young researchers, other with description
class FullEvent(BaseEvent):
    
    def __init__(self, ts_begin, ts_end, place_id, event_type, title_ru, title_en):
        self.sublist = []
        super().__init__(ts_begin, ts_end, place_id, event_type, title_ru, title_en)
    
    def __str__(self):
        return super().__str__()

    def full_str(self):
        result = ""
        result = super().__str__() + '\n' 
        for element in self.sublist:
            result = result + "Title:\n\t" + element[0] + '\n'
            if element[1] != "":
                result = result + "Authors:\n\t" + element[1] + '\n'
            if element[2] != "":
                result = result + "Speaker:\n\t" + element[2] + '\n'
        return result

class Plenary(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin, ts_end, place_id, "Plenary", title_ru, title_en)

class Research(FullEvent):

    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin, ts_end, place_id, "Research", title_ru, title_en)
        

class Young(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin, ts_end, place_id, "Young", title_ru, title_en)

class OtherFull(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin,ts_end, place_id, "Other full events", title_ru, title_en)        
         


