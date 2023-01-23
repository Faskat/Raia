# КЕША 2.0
import os
import subprocess
import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
import webbrowser
import random
from num2t4ru.num2t4ru import num2text
import psutil


print(f"{config.VA_NAME} (v{config.VA_VER}) Уже тут...")


def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2text(now.hour) + " " + num2text(now.minute)
        tts.va_speak(text)


    elif cmd == 'open_browser':
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open("http://python.org")

    elif cmd == 'reboot':
        text = "Компьютер перезагружается"
        tts.va_speak(text)
        os.system("shutdown /r /t 1")

    elif cmd == 'sleep':
        text = "Компьютер перешел в режим сна"
        tts.va_speak(text)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif cmd == 'shutdown':
        text = "Компьютер выключается"
        tts.va_speak(text)
        os.system("shutdown /p")

    elif cmd == 'open calc':
        text = "запускаю калькулятор"
        tts.va_speak(text)
        os.system("calc.exe")

    elif cmd == 'close_calculator':
        text = "Закрываю калькулятор"
        tts.va_speak(text)
        for process in psutil.process_iter():
            if process.name() == 'CalculatorApp.exe':
                process.kill()

    elif cmd == 'close_telegram':
        text = "Закрываю телеграмм"
        tts.va_speak(text)
        for process in psutil.process_iter():
            if process.name() == 'Telegram.exe':
                process.kill()

    elif cmd == 'close_viber':
        text = "Закрываю вайбер"
        tts.va_speak(text)
        for process in psutil.process_iter():
            if process.name() == 'Viber.exe':
                process.kill()

# начать прослушивание команд
stt.va_listen(va_respond)