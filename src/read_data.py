from classes import BaseEvent, SimpleEvent, FullEvent, Food, Other, Plenary, Research, Young, OtherFull
from datetime import datetime
import time
from docx import Document
import re
import sys
import pickle
import jsonpickle
import json

def get_place_id(string):
    places = {
    "Sokolniki" : 0,
    "Сокольники" : 0,
    "Passage" : 1,
    "Пассаж" : 1,
    "Москва" : 2,
    "Moskva" : 2,
    "Okhotny" : 3,
    "Охотный" : 3,
    "Krymsky" : 4,
    "Крымский" : 4,
    "Vorobiovy" : 5,
    "Воробьевы" : 5,
    "Воробьёвы" : 5,
    "Arbat" : 6,
    "Арбат" : 6,
    "Krasnye" : 7,
    "Красные": 7,
    "Ostozhenka" : 8,
    "Остоженка" : 8,
    "Chistye" : 9,
    "Чистые" : 9,
    "Polyanka" : 10,
    "Полянка" : 10,
    "Maroseika" : 11,
    "Маросейка" : 11,
    } 
    
    string = re.sub('[«»“”]', '', string)
    for word in string.split(" "):

        if word in places:
            return places[word]
    return -1

def get_timestamp(date, hours, minutes):
    ''' date is day(int), hours and minutes are also (int)'''
    from datetime import datetime
    import time
    dt = datetime(year = 2018,month= 9,day= date, hour = hours, minute = minutes)
    return time.mktime(dt.timetuple())




if __name__ == '__main__':

    if len(sys.argv) == 1:
        mode = 'print'
    elif len(sys.argv) == 2 and (sys.argv[1] == 'json' or sys.argv[1] == 'pickle'):
        mode = sys.argv[1]
    else:
        sys.exit("Usage: python3 classes.py [pickle / json]\nDefault is printing.")


    document = Document("../Program-2018_v4.docx")
    doc_length = len(document.paragraphs)

    event_list = []
    for i in range(1,doc_length):
        text = document.paragraphs[i].text

        if "Понедельник" in text:
            current_date = 24
        elif "Вторник" in text:
            current_date = 25
        else:
            continue
        if "Poster" in text:
            continue
        if (document.paragraphs[i+1].text) == "": #leaving tables out
           continue

        current_time = document.paragraphs[i].text.split()[3]
        current_place = get_place_id(document.paragraphs[i+1].text)
        #getting timestamps from begin and end times
        begin = current_time.split('-')[0]
        end = current_time.split('-')[1]
        
        ts_begin = get_timestamp(current_date, int(begin.split(':')[0]), int(begin.split(':')[1]))
        ts_end = get_timestamp(current_date, int(end.split(':')[0]), int(end.split(':')[1]))

        title_ru = document.paragraphs[i+2].text.split("//")[0]
        if "//" in document.paragraphs[i+2].text:
            title_en = document.paragraphs[i+2].text.split("//")[1]
            if title_en[0] == " ":
                title_en = title_en[1:] #cleaning one space in the beginning
        else:
            title_en = title_ru
        title_ru = title_ru.rstrip()
        #now deciding which object to create
        if any(substring in title_en for substring in ["Lunch", "Reception", "Coffee"]):
            event = Food(ts_begin, ts_end, current_place, title_ru, title_en)

        elif "Plenary" in title_en:
            event = Plenary(ts_begin, ts_end, current_place, title_ru, title_en)

        elif "Research" in title_en:
            event = Research(ts_begin, ts_end, current_place, title_ru, title_en)

        elif "Student" in title_en:
            event = Young(ts_begin, ts_end, current_place, title_ru, title_en)  

        elif "Awards" in title_en:
            event = Other(ts_begin, ts_end, current_place, title_ru, title_en)
        
        else:
            #now checking if list of talks is needed
            j = 1
            list_needed = 0
            while not "//" in document.paragraphs[i+2+j].text:
                for run in  document.paragraphs[i+2+j].runs:
                    if run.bold:
                        list_needed = 1
                j = j + 1
            if list_needed:
                event = OtherFull(ts_begin, ts_end, current_place, title_ru, title_en)
            else:
                event = Other(ts_begin, ts_end, current_place, title_ru, title_en)

        if isinstance(event, FullEvent) or isinstance(event, Other):
            #filling the list of talks
            talks_list = []
            j = 1
            while not "//" in document.paragraphs[i+2+j].text:
                talks_list = talks_list + document.paragraphs[i+2+j].runs
                j = j + 1

            j = 1    
            while j < len(talks_list): #clearing list of talks
                talks_list[j].text = talks_list[j].text.rstrip()
                if talks_list[j].text == '':
                    del(talks_list[j])
                j = j + 1

            j = 1    
            while j < len(talks_list): #looking for talks and authors
                if talks_list[j].bold:
                    current_talk = talks_list[j].text
                    current_talk = current_talk.strip('\n')
                    current_authors = ""
                    current_speaker = ""
                    k = 1
                    while (j+k < len(talks_list)) and (not talks_list[j+k].bold): 
                        if talks_list[j+k].underline:
                            current_speaker = talks_list[j+k].text
                        if talks_list[j+k].font.superscript:
                            k = k + 1
                            continue
                        current_authors = current_authors +  talks_list[j+k].text.strip('\n')

                        k = k + 1
                    event.sublist.append((current_talk, current_authors, current_speaker))

                j = j + 1

        if isinstance(event, Other): #Looking for description
            description_lines = []
            description = ""
            j = 1
            while not "//" in document.paragraphs[i+2+j].text:
                description_lines = description_lines + document.paragraphs[i+2+j].runs
                j = j + 1
            for t in description_lines:
                t.text = t.text.strip()
                t.text = t.text.strip('\n')
                if t.text != '':    
                    description += t.text + '\n'
            if description != "":
                event.description = description
        
        event_list.append(event)


    if mode == 'print':
        for event in event_list:
            print(event)
            print("================")
    elif mode == 'pickle':
        with open('../event_list.pickle', 'wb') as f:
            pickle.dump(event_list, f, pickle.HIGHEST_PROTOCOL)  
    elif mode == 'json':
        
        with open('../event_list.json', 'w') as f:
            for event in event_list:
                f.write(jsonpickle.encode(event))
                f.write('\n')