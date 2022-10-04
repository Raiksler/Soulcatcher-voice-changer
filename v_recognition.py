import subprocess
import speech_recognition as sr

def voice_to_text(file):  # Конвертация аудиосообщения в формат wav и его распознавание.
    subprocess.call(['ffmpeg', '-i', 'temp/{file_name}'.format(file_name = file), 'temp/{file_name}.wav'.format(file_name = file[0:-4])])
    file = 'temp/{file_name}.wav'.format(file_name = file[0:-4])

    recognizer = sr.Recognizer() # Определяем распознаватель речи.
    file = sr.AudioFile(file)    # Создаем инстанс для распознавания
    with file as sourse:
        audio = recognizer.record(sourse)

    return recognizer.recognize_google(audio, language='ru-RU') # Непосредственно распознавание. Выбираем API, файл и язык.