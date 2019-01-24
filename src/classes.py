from datetime import datetime


class BaseEvent(object):

    def __init__(self, ts_begin, ts_end, place_id, event_type, title_ru, title_en):
        self.ts_begin = ts_begin
        self.ts_end = ts_end
        self.place_id = place_id
        self.event_type = event_type
        self.title_ru = title_ru
        self.title_en = title_en
    def __str__(self):
        return "" + str(datetime.fromtimestamp(self.ts_begin)) + " " + str(self.place_id) + " " + str(self.event_type) + " " + str(self.title_ru) + " " + str(self.title_en)

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
         super().__init__(ts_begin, ts_end, place_id, "Other", title_ru, title_en)

#Events with description: Plenary session, research session, Young researchers, other with description
class FullEvent(BaseEvent):
    
    def __init__(self, ts_begin, ts_end, place_id, event_type, title_ru, title_en):
        self.sublist = []
        super().__init__(ts_begin, ts_end, place_id, event_type, title_ru, title_en)
    
    def __str__(self):
        result = ""
        result = super().__str__() + '\n' 
        for element in self.sublist:
            result = result + "Title:\n\t" + element[0] + '\n'
            result = result + "Authors\n\t" + element[1] + '\n'
        return result

class Plenary(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin, ts_end, place_id, "Plenary", title_ru, title_en)

class Research(FullEvent):

    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin, ts_end, place_id, "Research", title_ru, title_en)
        

class Young(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin, ts_end, place_id, "Young researchers", title_ru, title_en)

class OtherFull(FullEvent):
    def __init__(self, ts_begin, ts_end, place_id, title_ru, title_en):
         super().__init__(ts_begin,ts_end, place_id, "Other full events", title_ru, title_en)        
         


