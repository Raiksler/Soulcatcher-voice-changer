import asyncio
import types
import requests
import urllib.request
import aiogram
from aiogram import Bot, Dispatcher, types
import env
import responses

bot = Bot(token=env.telegram_token)
dp = Dispatcher(bot)                                           # Диспетчер. Обрабатывает апдейты приходящие боту.

async def cmd_start(message: types.Message):
    await message.answer(responses.start)

async def voice_handler(message: types.Voice):
    await message.answer('Voice captured!')
    file_id = message['voice']['file_id']
    file_path = requests.get('https://api.telegram.org/bot{token}/getFile?file_id={id}'.format(token = env.telegram_token, id = file_id)).json()['result']['file_path']
    file_response = requests.get('https://api.telegram.org/file/bot{token}/{path}'.format(token = env.telegram_token, path = file_path))
    if file_response.status_code == 200:
        with open('temp/{name}'.format(name = file_path), 'wb') as dl_dir:
            dl_dir.write(file_response.content)

async def main():                                              # Основной модуль, он же диспетчер. Обращение к лонгполлу и регистрация хэндлеров
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(voice_handler, content_types=types.ContentType.VOICE)
    await dp.start_polling()                                   # Обращение к лонгполл телеграма. Если будет зарегистрирован апдейт, попадающий под фильтры одного из хэндлеров, будет активирован соответствующий хэндлер.

if __name__ == '__main__':
    asyncio.run(main())