import asyncio
from statistics import mode
import types
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import env
import responses
import v_recognition



class Modes(StatesGroup):
    voice_recognition = State()
    voice_tone_change = State()



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



async def voice_handler(message: types.Voice):                 # Получение голосового сообщения и скачивание его на сервер.
    await message.answer('Voice captured!')
    file_id = message['voice']['file_id']
    file_path = requests.get('https://api.telegram.org/bot{token}/getFile?file_id={id}'.format(token = env.telegram_token, id = file_id)).json()['result']['file_path']
    file_response = requests.get('https://api.telegram.org/file/bot{token}/{path}'.format(token = env.telegram_token, path = file_path))
    if file_response.status_code == 200:
        with open('temp/{name}'.format(name = file_path), 'wb') as dl_dir:
            dl_dir.write(file_response.content)
            text = v_recognition.voice_to_text(file_path)      # Конвертация голосового сообщения в текст.
            await message.answer(text)

async def change_tone(message: types.Voice):
    await message.answer('Change tone placeholder!')



async def main():                                              # Основной модуль, он же диспетчер. Обращение к лонгполлу и регистрация хэндлеров
    dp.register_message_handler(cmd_start, commands=["start"], state="*")
    dp.register_message_handler(cmd_help, commands=["help"], state="*")
    dp.register_message_handler(cmd_pitch, commands=["pitch"], state="*")
    dp.register_message_handler(cmd_recognite, commands=["recognite"], state="*")
    dp.register_message_handler(change_tone, content_types=types.ContentType.VOICE, state=Modes.voice_tone_change)
    dp.register_message_handler(voice_handler, content_types=types.ContentType.VOICE, state=Modes.voice_recognition)
    await dp.start_polling()                                   # Обращение к лонгполл телеграма. Если будет зарегистрирован апдейт, попадающий под фильтры одного из хэндлеров, будет активирован соответствующий хэндлер.


storage = MemoryStorage()
bot = Bot(token=env.telegram_token)
dp = Dispatcher(bot, storage=storage)                                           # Диспетчер. Обрабатывает апдейты приходящие боту.

if __name__ == '__main__':
    asyncio.run(main())