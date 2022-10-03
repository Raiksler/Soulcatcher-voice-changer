import asyncio
import types
import aiogram
from aiogram import Bot, Dispatcher, types
import env
import responses

bot = Bot(token=env.telegram_token)
dp = Dispatcher(bot)                                           # Диспетчер. Обрабатывает апдейты приходящие боту.

async def cmd_start(message: types.Message):
    await message.answer(responses.start)

async def analyser(message):
    await message.answer(message)
    await message.answer(type(message))

async def voice_handler(message: types.Voice):
    await message.answer('Voice captured!')

async def main():                                              # Основной модуль, он же диспетчер. Обращение к лонгполлу и регистрация хэндлеров
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(analyser, content_types=types.ContentType.VOICE)
    await dp.start_polling()                                   # Обращение к лонгполл телеграма. Если будет зарегистрирован апдейт, попадающий под фильтры одного из хэндлеров, будет активирован соответствующий хэндлер.

if __name__ == '__main__':
    asyncio.run(main())