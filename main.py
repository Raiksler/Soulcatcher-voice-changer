import asyncio
from email.message import Message
import types
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import env
import responses
import voice_works



class Modes(StatesGroup):                                       # Три стейта - три режима работы бота.
    voice_recognition = State()
    voice_tone_change = State()
    text_to_speech = State()



async def cmd_start(message: types.Message):
    await message.answer(responses.start)

async def cmd_help(message: types.Message):
    await message.answer(responses.help)

async def cmd_pitch(message: types.Message):
    await message.answer(responses.pitch)
    await Modes.voice_tone_change.set()

async def cmd_recognite(message: types.Message):
    await message.answer(responses.recognition)
    await Modes.voice_recognition.set()

async def cmd_text_to_speech(message: types.Message):
    await message.answer(responses.text_to_speech)
    await Modes.text_to_speech.set()

async def voice_recogniser(message: types.Voice):
    await message.answer('Обработка аудио...')
    file = voice_works.get_voice_file(message, get_name=True)                 # Скачивание голосового сообщения на сервер для дальнейшей обработки.
    text = voice_works.voice_to_text(file[0])                     # Конвертация голосового сообщения в текст.
    if text == "Empty v_msg":
        await message.answer('Голосовое сообщение не содержит слов или слова не распознаны.')
        await voice_works.eraser(file[1], mode='recognite')
    else:
        await message.answer(text)
        await voice_works.eraser(file[1], mode='recognite')

async def text_to_speech_handler(message: types.Message):
    await message.answer('Обработка аудио...')
    file = voice_works.get_voice_file(message, get_name=True)
    text = voice_works.voice_to_text(file[0])
    if text == "Empty v_msg":
        await message.answer('Голосовое сообщение не содержит слов или слова не распознаны.')
        await voice_works.eraser(file[1], mode='recognite')
    else:
        voice_works.text_to_speech(text, file[1])
        machine_audio = open('temp/machine/{name}.ogg'.format(name = file[1]), 'rb')        # Отправляем обработанное голосовое. Не забываем открыть.
        await message.answer_voice(voice=machine_audio)
        machine_audio.close()                                                               # И закрыть
        await voice_works.eraser(file[1], mode='resound')          

async def change_tone(message: types.Voice):
    await message.answer('Обработка аудио...')
    file = voice_works.get_voice_file(message, get_name=True)
    await voice_works.change_pitch(file[0], file[1])
    reworked_audio = open('temp/voice/{file}.ogg'.format(file=file[1]), 'rb')
    await message.answer_voice(voice=reworked_audio)
    reworked_audio.close()
    await voice_works.eraser(file[1], mode='pitch')


async def main():                                              # Основной модуль, он же диспетчер. Обращение к лонгполлу и регистрация хэндлеров
    dp.register_message_handler(cmd_start, commands=["start"], state="*")
    dp.register_message_handler(cmd_help, commands=["help"], state="*")
    dp.register_message_handler(cmd_pitch, commands=["pitch"], state="*")
    dp.register_message_handler(cmd_recognite, commands=["recognite"], state="*")
    dp.register_message_handler(cmd_text_to_speech, commands=['resound'], state="*")
    dp.register_message_handler(change_tone, content_types=types.ContentType.VOICE, state=Modes.voice_tone_change)
    dp.register_message_handler(voice_recogniser, content_types=types.ContentType.VOICE, state=Modes.voice_recognition)
    dp.register_message_handler(text_to_speech_handler, content_types=types.ContentType.VOICE, state=Modes.text_to_speech)
    await dp.start_polling()                                   # Обращение к лонгполл телеграма. Если будет зарегистрирован апдейт, попадающий под фильтры одного из хэндлеров, будет активирован соответствующий хэндлер.


storage = MemoryStorage()
bot = Bot(token=env.telegram_token)
dp = Dispatcher(bot, storage=storage)                                           # Диспетчер. Обрабатывает апдейты приходящие боту.

if __name__ == '__main__':
    asyncio.run(main())