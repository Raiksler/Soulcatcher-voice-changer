import asyncio
import types
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from emoji import emojize
import env
import responses
import voice_works
import translate_works



class Modes(StatesGroup):                                       # Стейты для каждого режима работы бота.
    voice_tone_change = State()
    translate_text = State()
    text_to_speech = State()

    voice_recognition = State()  # Распознавание речи, основное состояние, выбор языка. Далее идут стейты для различных языков.
    voice_recognition_ru = State()
    voice_recognition_en = State()
    voice_recognition_fr = State()
    voice_recognition_de = State()
    voice_recognition_id = State()
    voice_recognition_pt = State()
    voice_recognition_es = State()
    voice_recognition_hi = State()
    voice_recognition_tr = State()



async def cmd_start(message: types.Message):
    await message.answer(responses.start)

async def cmd_help(message: types.Message):
    await message.answer(responses.help)

async def cmd_changelog(message: types.Message):
    await message.answer(responses.changelog)

async def cmd_pitch(message: types.Message):
    await message.answer(responses.pitch)
    await Modes.voice_tone_change.set()

async def cmd_recognite(message: types.Message):
    await message.answer(responses.recognition)

async def cmd_text_to_speech(message: types.Message):
    await message.answer(responses.text_to_speech)
    await Modes.text_to_speech.set()

async def cmd_translate_text(message: types.Message):
    await message.answer(responses.translate_text)
    await Modes.translate_text.set()

async def cmd_recognite_lg_choice(message: types.Message):
    await message.answer(responses.chosen_lg_to_recognite(message.text))
    modes = {"/r_ru" : Modes.voice_recognition_ru.set, "/r_en" : Modes.voice_recognition_en.set, "/r_fr" : Modes.voice_recognition_fr.set, "/r_de" : Modes.voice_recognition_de.set, "/r_id" : Modes.voice_recognition_id.set, "/r_pt" : Modes.voice_recognition_pt.set, "/r_es" : Modes.voice_recognition_es.set, "/r_in" : Modes.voice_recognition_hi.set, "/r_tr" : Modes.voice_recognition_tr.set}
    await modes[message.text]()

async def voice_recogniser(message: types.Voice):
    languages = {'Modes:voice_recognition_ru' : 'ru-RU', 'Modes:voice_recognition_en' : 'en-US', 'Modes:voice_recognition_fr' : 'fr-FR', 'Modes:voice_recognition_de' : 'de_DE' ,'Modes:voice_recognition_id' : 'id-ID', 'Modes:voice_recognition_pt' : 'pt-PT', 'Modes:voice_recognition_es' : 'es-ES', 'Modes:voice_recognition_hi' : 'hi-IN', 'Modes:voice_recognition_tr' : 'tr'}
    recognition_lang = languages[await storage.get_state(user=message.from_id, chat=message.chat.id)]   # Достаем стейт, для выбора языка распознавания.
    status_msg = await message.answer('Обработка аудио...')
    file = voice_works.get_voice_file(message, get_name=True)                 # Скачивание голосового сообщения на сервер для дальнейшей обработки.
    text = voice_works.voice_to_text(file[0], language=recognition_lang)                     # Конвертация голосового сообщения в текст.
    if text == "Empty v_msg":
        await status_msg.delete()
        await message.answer('Голосовое сообщение не содержит слов или слова не распознаны.')
        await voice_works.eraser(file[1], mode='recognite')
    else:
        await status_msg.delete()
        await message.answer(text)
        await voice_works.eraser(file[1], mode='recognite')

async def text_to_speech_handler(message: types.Message):
    status_msg = await message.answer('Обработка аудио...')
    file = voice_works.get_voice_file(message, get_name=True)
    text = voice_works.voice_to_text(file[0])
    if text == "Empty v_msg":
        await status_msg.delete()
        await message.answer('Голосовое сообщение не содержит слов или слова не распознаны.')
        await voice_works.eraser(file[1], mode='recognite')
    else:
        voice_works.text_to_speech(text, file[1])
        machine_audio = open('temp/machine/{name}.ogg'.format(name = file[1]), 'rb')        # Отправляем обработанное голосовое. Не забываем открыть.
        await status_msg.delete()
        await message.answer_voice(voice=machine_audio)
        machine_audio.close()                                                               # И закрыть
        await voice_works.eraser(file[1], mode='resound')          

async def change_tone(message: types.Voice):
    status_msg = await message.answer('Обработка аудио...')
    file = voice_works.get_voice_file(message, get_name=True)
    await voice_works.change_pitch(file[0], file[1])
    reworked_audio = open('temp/voice/{file}.ogg'.format(file=file[1]), 'rb')
    await status_msg.delete()
    await message.answer_voice(voice=reworked_audio)
    reworked_audio.close()
    await voice_works.eraser(file[1], mode='pitch')

async def translate_text(message: types.Message):
    status_msg = await message.answer('Идет перевод текста...')
    result = await translate_works.translate(text=message.text, to_language=message['from']['language_code'])
    if result['code'] == "en":
        result['code'] = "gb"
    await status_msg.delete()
    await message.answer(emojize(responses.format_translation(result)))





async def main():                                              # Основной модуль, он же диспетчер. Обращение к лонгполлу и регистрация хэндлеров
    dp.register_message_handler(cmd_start, commands=["start"], state="*")
    dp.register_message_handler(cmd_help, commands=["help"], state="*")
    dp.register_message_handler(cmd_changelog, commands=["changelog"], state ="*")
    dp.register_message_handler(cmd_pitch, commands=["pitch"], state="*")
    dp.register_message_handler(cmd_recognite, commands=["recognite"], state="*")
    dp.register_message_handler(cmd_recognite_lg_choice, commands=["r_ru", "r_en", "r_fr", "r_de", "r_id", "r_pt", "r_es", "r_in", "r_tr"], state="*")
    dp.register_message_handler(cmd_text_to_speech, commands=['resound'], state="*")
    dp.register_message_handler(cmd_translate_text, commands=['translate'], state="*")
    dp.register_message_handler(change_tone, content_types=types.ContentType.VOICE, state=Modes.voice_tone_change)
    dp.register_message_handler(voice_recogniser, content_types=types.ContentType.VOICE, state=[Modes.voice_recognition_ru, Modes.voice_recognition_en, Modes.voice_recognition_fr,Modes.voice_recognition_de,Modes.voice_recognition_id,Modes.voice_recognition_pt,Modes.voice_recognition_es,Modes.voice_recognition_hi,Modes.voice_recognition_tr])
    dp.register_message_handler(text_to_speech_handler, content_types=types.ContentType.VOICE, state=Modes.text_to_speech)
    dp.register_message_handler(translate_text, content_types=types.ContentType.TEXT, state=Modes.translate_text)
    await dp.start_polling()                                   # Обращение к лонгполл телеграма. Если будет зарегистрирован апдейт, попадающий под фильтры одного из хэндлеров, будет активирован соответствующий хэндлер.


storage = MemoryStorage()
bot = Bot(token=env.telegram_token)
dp = Dispatcher(bot, storage=storage)                                           # Диспетчер. Обрабатывает апдейты приходящие боту.

if __name__ == '__main__':
    asyncio.run(main())