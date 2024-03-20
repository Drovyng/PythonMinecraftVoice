import os, winsound
commands = {
    "атака": "Левый клик",
    "левый клик": "Левый клик\n",
    "средний клик": "Средний клик\n",

    "правый клик": "Правый клик",
    "взаимодействие": "Правый клик\n",

    "дабл клик": "Двойной левый клик\n\n",


    "закликивание": "Включает автокликер",
    "кликать": "Включает автокликер\n",
    "не закликивание": "Выключает автокликер",
    "не кликать": "Выключает автокликер\n\n\n\n-----------Перемещение-----------\n\n\n",


    "вперёд": "Идёт вперёд (W)",
    "не вперёд": "Не идти вперёд (W)\n",

    "назад": "Идёт назад (S)",
    "не назад": "Не идти назад (S)\n",

    "прыг": "Прыгнуть",
    "прыжок": "Прыгнуть\n",

    "сесть": "Сесть (SHIFT)",
    "встать": "Встать (SHIFT)\n",

    "плыть": "Начать прыгать",
    "не плыть": "Перестать прыгать\n\n\n\n------------Действия------------\n\n\n",


    "крафт": "Открывает инвентарь (E)",
    "меню": "Открывает меню (ESCAPE)\n\n",


    "копать": "Начинает копать блоки",
    "ломать": "Начинает копать блоки\n",

    "не копать": "Перестаёт копать блоки",
    "не ломать": "Перестаёт копать блоки\n",

    "строить": "Начинает строить блоки",
    "не строить": "Перестаёт строить блоки\n\n",


    "стоп": "Останавливает все действия\n\n\n\n-------------Камера-------------\n\n\n",


    "лево": "Перемещает мышь влево",
    "право": "Перемещает мышь вправо",
    "верх": "Перемещает мышь вверх",
    "низ": "Перемещает мышь вниз\n",

    "мини лево": "Слабо перемещает мышь влево",
    "мини право": "Слабо перемещает мышь вправо",
    "мини верх": "Слабо перемещает мышь вверх",
    "мини вниз": "Слабо перемещает мышь вниз\n\n",


    "сильнее": "Делает управление мышкой сильнее на 1/4",
    "слабее": "Делает управление мышкой слабее на 1/4\n",

    "намного сильнее": "Делает управление мышкой сильнее на 1/2",
    "намного слабее": "Делает управление мышкой слабее на 1/2\n",

    "супер сильно": "Делает управление мышкой сильнее на 1",
    "супер слабо": "Делает управление мышкой слабее на 1\n",

    "сброс силы": "Сбрасывает силу управления мышкой\n\n\n\n---------Дополнительное---------\n\n\n",


    "один": "Слот 1",
    "два": "Слот 2",
    "три": "Слот 3",
    "четыре": "Слот 4",
    "пять": "Слот 5",
    "шесть": "Слот 6",
    "семь": "Слот 7",
    "восемь": "Слот 8",
    "девять": "Слот 9\n\n",

    "выключить": "Выключает программу\n\n--------Конец Инструкции--------\n"
}
if os.path.exists("required") or not os.path.isdir("required"):
    print("\nНЕ НАЙДЕНА ПАПКА \"required\", БЕЗ НЕЁ ПРОГРАММА НЕ ЗАПУСТИТСЯ!!!\n")
    os.system("pause")
    exit(1)
print("\n-----Список Голосовых Команд-----\n")
for key in commands:
    value = commands[key]
    newPage = value.find("\n\n\n\n")
    if newPage > 0:
        value = value[:-2]
        print(f"[{key}]: {value[:newPage+2]}")
        os.system("pause")
        print(f"{value[newPage+3:]}")
    else:
        print(f"[{key}]: {value}")

def play_ok():
    winsound.MessageBeep(winsound.MB_OK)

os.system("pause")

play_ok()

import json, pyaudio, keyboard, mouse, threading
import time

from vosk import Model, KaldiRecognizer
from fuzzywuzzy import fuzz

model = Model('required')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

class SharedData():
    def __init__(self):
        self.autoclicker = False
        self.running = True

def another_thread_func(shared_data: SharedData):
    while shared_data.running:
        if shared_data.autoclicker:
            mouse.click("left")

        time.sleep(0.2)



shared_data = SharedData()

another_thread = threading.Thread(target=another_thread_func, args=(shared_data, ))
another_thread.start()

def listen():
    global shared_data
    while shared_data.running:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']

nums = [
    "один",
    "два",
    "три",
    "четыре",
    "пять",
    "шесть",
    "семь",
    "восемь",
    "девять"
]


move_power = 1.0

def move_mouse(x, y, scale):
    global move_power
    for i in range(int(float(scale) * move_power // 5)):
        mouse._os_mouse.move_relative(x * 5, y * 5)
        time.sleep(0.0075)

def check_text(text: str):
    global commands, move_power, nums, shared_data
    text = text.lower()

    percents = {}


    for key in list(commands.keys()):
        percents[key] = fuzz.ratio(text, key)

    sortedPercents = {k: v for k, v in sorted(percents.items(), key=lambda item: -item[1])}

    if list(sortedPercents.values())[0] < 50:
        return

    command = list(sortedPercents.keys())[0]

    if command == "средний клик":
        mouse.click("middle")

    if command == "правый клик" or command == "взаимодействие":
        mouse.click("right")

    if command == "левый клик" or command == "атака":
        mouse.click("left")

    if command == "дабл клик":
        mouse.click("left")
        time.sleep(0.05)
        mouse.click("left")



    if command == "не вперёд" or command == "стоп":
        keyboard.release("w")

    if command == "вперёд":
        keyboard.press("w")

    if command == "не назад" or command == "стоп":
        keyboard.release("s")

    if command == "назад":
        keyboard.press("s")

    if command == "прыг" or command == "прыжок":
        keyboard.press("space")
        time.sleep(0.1)
        keyboard.release("space")

    if command == "не плыть" or command == "стоп":
        keyboard.release("space")

    if command == "плыть":
        keyboard.press("space")

    if command == "сесть":
        keyboard.press("shift")

    if command == "встать" or command == "стоп":
        keyboard.release("shift")


    if command == "мини лево":
        move_mouse(-1, 0, 25)

    if command == "мини право":
        move_mouse(1, 0, 25)

    if command == "мини верх":
        move_mouse(0, -1, 25)

    if command == "мини низ":
        move_mouse(0, 1, 25)



    if command == "лево":
        move_mouse(-1, 0, 100)

    if command == "право":
        move_mouse(1, 0, 100)

    if command == "верх":
        move_mouse(0, -1, 100)

    if command == "низ":
        move_mouse(0, 1, 100)


    if command == "крафт":
        keyboard.press_and_release("e")
    if command == "меню":
        keyboard.press_and_release("escape")


    if command == "копать" or command == "ломать":
        mouse.press("left")
    if command == "не копать" or command == "не ломать" or command == "стоп":
        mouse.release("left")


    if command == "строить":
        mouse.press("right")
    if command == "не строить" or command == "стоп":
        mouse.release("right")


    if command == "сильнее":
        move_power += 0.25
        play_ok()
    if command == "слабее":
        move_power -= 0.25
        play_ok()

    if command == "намного сильнее":
        move_power += 0.5
        play_ok()
    if command == "намного слабее":
        move_power -= 0.5
        play_ok()

    if command == "супер сильно":
        move_power += 1
        play_ok()
    if command == "супер слабо":
        move_power -= 1
        play_ok()
    if command == "сброс силы":
        move_power = 1
        play_ok()

    if command == "закликивание" or command == "кликать":
        shared_data.autoclicker = True
    if command == "не закликивание" or command == "не кликать" or command == "стоп":
        shared_data.autoclicker = False

    if command in nums:
        keyboard.press_and_release(f"{(nums.index(command)+1)}")

    if command == "стоп":
        play_ok()

    if command == "выключить":
        play_ok()
        shared_data.running = False
        another_thread.join()
        print(f"Команда - [выключить]")
        exit(0)


    print(f"Команда - [{command}]")




for text in listen():
    print(text)
    check_text(text)

