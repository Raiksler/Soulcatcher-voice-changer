import subprocess
import requests
import re
import os
from random import choice
import speech_recognition as sr
from gtts import gTTS
import env

def voice_to_text(file):                                                # Конвертация аудиосообщения в формат wav и его распознавание.
    subprocess.call(['ffmpeg', '-i', 'temp/{file_name}'.format(file_name = file), 'temp/{file_name}.wav'.format(file_name = file[0:-4])])
    file = 'temp/{file_name}.wav'.format(file_name = file[0:-4])
    recognizer = sr.Recognizer()                                        # Определяем распознаватель речи.
    file = sr.AudioFile(file)                                           # Создаем инстанс для распознавания
    with file as sourse:
        audio = recognizer.record(sourse)
    return recognizer.recognize_google(audio, language='ru-RU')         # Непосредственно распознавание. Выбираем API, файл и язык.

def text_to_speech(text, name):
    var = gTTS(text=text, lang='ru')
    var.save('temp/machine/{name}.mp3'.format(name = name))
    subprocess.call(['ffmpeg', '-i', 'temp/machine/{name}.mp3'.format(name = name), '-c:a', 'libopus', 'temp/machine/{name}.ogg'.format(name = name)])


def get_voice_file(message, get_name=False):              
    file_id = message['voice']['file_id']
    file_path = requests.get('https://api.telegram.org/bot{token}/getFile?file_id={id}'.format(token = env.telegram_token, id = file_id)).json()['result']['file_path']
    file_response = requests.get('https://api.telegram.org/file/bot{token}/{path}'.format(token = env.telegram_token, path = file_path))
    if file_response.status_code == 200:
        with open('temp/{name}'.format(name = file_path), 'wb') as dl_dir:
            dl_dir.write(file_response.content)
            if get_name == False:
                return file_path
            else:
                file_name = re.search(r'f.+', file_path).group(0)[0:-4]
                return (file_path, file_name)

async def change_pitch(file, name):
    pitch = choice([0.8, 0.85, 0.9, 1.15, 1.20, 1.25])
    subprocess.call(['ffmpeg', '-i', 'temp/voice/{name}.oga'.format(name=name), '-af', 'asetrate=44100*{pitch},aresample=44100,atempo=1/{pitch}'.format(pitch=pitch), 'temp/voice/{name}.ogg'.format(name=name)])

async def eraser(file, mode):                                     #Освобождает папку temp после обработки.
    if mode == 'recognite':
        os.remove('temp/voice/{file}.wav'.format(file=file))
        os.remove('temp/voice/{file}.oga'.format(file=file))
    elif mode == 'pitch':
        os.remove('temp/voice/{file}.oga'.format(file=file))
        os.remove('temp/voice/{file}.ogg'.format(file=file))
    elif mode == 'resound':
        os.remove('temp/voice/{file}.oga'.format(file=file))
        os.remove('temp/voice/{file}.wav'.format(file=file))
        os.remove('temp/machine/{file}.mp3'.format(file=file))
        os.remove('temp/machine/{file}.ogg'.format(file=file))
