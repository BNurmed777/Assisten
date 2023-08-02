import pyttsx3
import speech_recognition as sr
import colorama
from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
import configparser
import requests
from bs4 import BeautifulSoup
import re
import cv2 




class Assistant:
 
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
 
    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка
 
    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.text = ''
 
        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час'): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'вырубись'): self.quite,
            ('включи музыку', 'вруби музон', 'вруби музыку', 'включи музон', 'врубай музыку'): self.music,
            ('выключи компьютер', 'выруби компьютер'): self.shut,
            ('какая погода', 'погода', 'погода на улице', 'какая погода на улице'): self.weather,
            ('забавный факт', 'смешной факт', 'факт дня', 'интересный факт'): self.facts,
            ('перезагрузи компьютер', 'перезагрузи комп', 'перезагружай комп', 'перезагрузи'): self.restart_pc,
            ('расскажи анекдот', 'анекдот', 'пошути'): self.joke,
            ('забавный факт', 'смешной факт', 'факт дня', 'интересный факт'): self.facts,
            ('сколько лет','скажи возраст','помопас ос ьор'):self.let,
            ('у тебя есть друг','кто тебя создал'): self.men,
            ('сделай снимок','сделай фото','покажи меня'):self.rasimga_ol,
            ('покажи меня','ты меня видишь'):self.rasimga,

        }
        
        
 
        self.ndels = ['морган', 'морген', 'моргэн', 'морг', 'ладно', 'не могла бы ты', 'пожалуйста',
                      'текущее', 'сейчас']
 
        self.commands = [
            'текущее время', 'сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'вырубись',
            'выключи компьютер', 'выруби компьютер',
            'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
        ]
 
        self.num_task = 0
        self.j = 0
        self.ans = ''





    def rasimga(self):        
        cap = cv2.VideoCapture(0)

        while True:
            ret, img = cap.read()
            cv2.imshow("From camera", img)
            k=cv2.waitKey(30) & 0xFF
            if k == 27:
                break
            
        cap.release()
        cv2.destroyAllWindows()

    def rasimga_ol(self):
        cap = cv2.VideoCapture(0)

        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(30):
            cap.read()

        # Делаем снимок    
        ret, frame = cap.read()

        # Записываем в файл
        cv2.imwrite('cam.png', frame)   

        # Отключаем камеру
        cap.release()


    def men(self):
        self.talk('Нурмед')


 
    def let(self):
        text=pyttsx3.init()
       
        text.say(choice(['Mне много леть','Я старше тебя','возраст не имеет значения']))
        text.runAndWait()






    def facts(self):
        fact_url = "https://randstuff.ru/fact/"
        response = requests.get(fact_url)
        soup = BeautifulSoup(response.content, 'html.parser').findAll('td')
        items = list(soup)
        funny_fact = items[0]
        self.talk(str(funny_fact).replace('<td>', '').replace('</td>', '').replace('  ', ' '))
 




    def joke(self):
        link = requests.get('http://anekdotme.ru/random')
        parse = BeautifulSoup(link.text, "html.parser")
        select = parse.select('.anekdot_text')
        get = (select[0].getText().strip())
        reg = re.compile('[^a-zA-Zа-яА-я ^0-1-2-3-4-5-6-7-8-9:.,!?-]')
        joke = reg.sub('', get)
        self.talk(joke)



    def restart_pc(self):
        self.talk("Подтвердите действие!")
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
            self.talk('Действие подтверждено')
            self.talk('До скорых встреч!')
            system('shutdown /r /f /t 10 /c "Перезагрузка будет выполнена через 10 секунд"')
            self.quite()
        elif fuzz.ratio(text, 'отмена') > 60:
            self.talk("Действие не подтверждено")
        else:
            self.talk("Действие не подтверждено")


    def music(self):
        self.talk(choice(['Приятного прослушивания!', 'Наслаждайтесь!', 'Приятного прослушивания музыки']))
        music_list = ['https://www.youtube.com/watch?v=IjwBMrxlOOA', 'https://www.youtube.com/watch?v=qj3-riPaHx8',
                      'https://www.youtube.com/watch?v=8-_4pilz70c', 'https://www.youtube.com/watch?v=ebfboqfPYGk']
        webbrowser.open(choice(music_list))


    def cleaner(self, text):
        self.text = text
 
        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()
 
        self.ans = self.text
 
        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k > 70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k
 
        return str(self.ans)
 
    def recognizer(self):
        self.text = self.cleaner(self.listen())
        print(self.text)
 
        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):
            self.opener(self.text)
 
        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()
 
        self.engine.runAndWait()
        self.engine.stop()
 
    def time(self):
        now = datetime.datetime.now()
        self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
 
    def opener(self, task):
        links = {
            ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'контакт', 'vk'): 'https:vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
            ('insta', 'instagram', 'инста', 'инсту'): 'https://www.instagram.com/',
            ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил'): 'http://gmail.com/',
            ('python','питон','пайтин','питн','паййтн','пайт'): 'https://www.python.org/',

        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            self.talk('Открываю ' + double_task[i])
                            j += 1
                            break

    def cfile(self):
        try:
            cfr = Assistant.settings['SETTINGS']['fr']
            if cfr != 1:
                file = open('settings.ini', 'w', encoding='UTF-8')
                file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
                file.close()
        except Exception as e:
            print('Перезапустите Ассистента!', e)
            file = open('settings.ini', 'w', encoding='UTF-8')
            file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
            file.close()
 
    def quite(self):
        self.talk(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
        self.engine.stop()
        system('cls')
        sys.exit(0)
 
    def shut(self):
        self.talk("Подтвердите действие!")
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
            self.talk('Действие подтверждено')
            self.talk('До скорых встреч!')
            system('shutdown /s /f /t 10')
            self.quite()
        elif fuzz.ratio(text, 'отмена') > 60:
            self.talk("Действие не подтверждено")
        else:
            self.talk("Действие не подтверждено")
 
    def hello(self):
        self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую']))
 
    def weather(self):
 
        place = Assistant.settings['SETTINGS']['place']
        country = Assistant.settings['SETTINGS']['country']  # Переменная для записи страны/кода страны
        country_and_place = place + "Тахиата́ш ,Узбекистан " + country  # Запись города и страны в одну переменную через запятую
        owm = OWM('b125be9bdfb7cfdc1c4263a6b75803d8')  # Ваш ключ с сайта open weather map
        mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
        observation = mgr.weather_at_place(country_and_place)
        # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город
 
        w = observation.weather
 
        status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
        w.wind()  # Узнаем скорость ветра
        humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
        temp = w.temperature('celsius')[
            'temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
        self.talk("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
                  "\nТемпература " + str(
            round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
                  "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
                  "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")  # Узнаём и выводим скорость ветра
 
    def talk(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()
 
    def listen(self):
        with sr.Microphone() as source:
            a=pyttsx3.init()
            b='Я вас слушаю ...'
            a.say(b)
            a.runAndWait()
            print(colorama.Fore.LIGHTGREEN_EX + b)
            
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
            return self.text
 
 
Assistant().cfile()
 
 
while True:
    Assistant().recognizer()
 
