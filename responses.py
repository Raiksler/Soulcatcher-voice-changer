from emoji import emojize
import json
import gtts



class Responses:
    def __init__(self, lang_code):
        if lang_code == 'ru':
            self.start = emojize("Спасибо за использование Soulcatcher!\n\nБот предназначен для распознавания, модификации или переозвучки голоса в голосовых сообщениях. На данный момент, бот умеет работать в четырех режимах:\n\n:microphone: - Распознавание текста в голосовых сообщениях.\n:robot: - Машинная переозвучка голосового сообщения.\n:ninja: - Изменение тональности голоса в голосовом сообщении.\n:scroll:❓ - Перевод текстовых сообщений.\n\n/help - для просмотра доступных команд и выбора режима работы.\n\n:frog: @Raiksler - связь с разработчиком.")
            self.help = emojize("/help - список команд.\n/changelog - список последних изменений.\n\nБот может работать в нескольких режимах, для начала работы, выберите один из режимов ниже и отправьте боту голосовое сообщение для обработки.\n\n/recognite - распознать текст в голосовом сообщении.\n\n/pitch - изменить тональность голосового сообщения.\n\n/resound - машинно переозвучить голосовое сообщение.\n\n/translate - перевести текст входящего текстового сообщения на ваш язык. Доступен перевод с 108 языков. Конечный язык зависит от языка, выбранного на вашем усройстве.\n\nДополнительные возможности:\n\n:check_mark: При работе в любом режиме, вы можете не только записывать голосовые сообщения непосредственно в боте, но и пересылать ему на обработку сообщения из других диалогов. Бот обработает их в выбранном режиме.\n\n:check_mark: Бота можно добавить в любую беседу, после чего, любой из его режимов можно будет использовать прямо из нее. Каждый участник беседы может переключить бота в нужный ему режим. Настройки бота, добавленного в беседу независимы для каждого участника. Для корректной работы, боту необходимо выдать права администратора.")
            self.pitch = emojize(":check_mark: Выбран режим смены тональности голоса.\n\nБот изменит тональность любого входящего голосового сообщения в случайном диапазоне.")
            self.recognition = emojize(":check_mark: Выбран режим распознавания голоса.\n\nДля начала работы, выберите язык распознаваемых сообщений. Доступны следующие варианты:\n\n:Russia: /r_ru - русский\n:United_Kingdom: /r_en - английский\n:France: /r_fr - французский\n:Germany: /r_de - немецкий\n:Indonesia: /r_id - индонезийский\n:Portugal: /r_pt - португальский\n:Spain: /r_es - испанский\n:India: /r_in - хинди\n:Turkey: /r_tr - турецкий")
            self.chosen_lg_to_recognite = emojize("Вы выбрали {lang} язык для распознавания. Бот попытается распознать текст любого входящего голосового сообщения.")
            self.text_to_speech = emojize(":check_mark: Режим машинной переозвучки запущен. Бот обработает любое записанное или пересланное голосовое сообщение.")
            self.translate_text = emojize(":check_mark: Выбран режим перевода текста.\n\nБот попытается перевести текст любого входящего текстового сообщения и вернет переведенный вариант.")
            self.changelog = emojize("Soulcatcher 1.2:\n\n:check_mark: Добавлен режим перевода текста, подробности по команде /help\n\n:check_mark: Распознавание речи, отныне, возможно с девяти языков. Подробности по команде /recognite.\n\n:check_mark: Поддержка русского и английского языков для интерфейса бота. Язык автоматически подстраивается под системный язык пользователя.\n\n:check_mark: Поддержка мультиязычности для машинной переозвучки.")
            self.processing_audio = "Обработка аудио..."
            self.empty_v_msg_error = "Голосовое сообщение не содержит слов или слова не распознаны."
            self.translation_proceessing = 'Идет перевод текста...'
            self.languages = {"/r_ru" : "русский", "/r_en" : "английский", "/r_fr" : "французский", "/r_de" : "немецкий", "/r_id" : "индонезийский", "/r_pt" : "португальский", "/r_es" : "испанский", "/r_in" : "индийский (хинди)", "/r_tr" : "турецкий"}

        else:
            self.start = emojize("Thank you for using Soulcatcher!\n\n This bot is designed to recognize, modify or re-voice voice messages. At the moment, Soulcatcher can work in four modes:\n\n:microphone: - Recognition of text in voice messages.\n:robot: - Machine re-voicing of voice messages.\n:ninja: - Modify tone of voice in a voice message.\n:scroll:❓ - Translation of text messages.\n\n/help - to view available commands and select mode.\n\n:frog: @Raiksler - communication with the developer.")
            self.help = emojize("/help - list of all commands.\n/changelog - list of recent changes.\n\nBot can work in several modes, select one of the modes below and send a voice message to the bot for processing.\n\n/recognite - recognize the text in the voice message.\n\n/pitch - change the tone of the voice message.\n\n/resound - machine re-sound the voice message.\n\n/translate - translate the text of incoming text message into your language. There are 108 languages available for translation. The final language depends on the language selected on your device.\n\nExtras:\n\n:check_mark: When working in any mode, you can not only record voice messages directly in the bot, but also send it for processing messages from other conversations. The bot will process them in the selected mode.\n\n:check_mark: The bot can be added to any conversation, and then any of its modes can be used directly from it. Each participant of the conversation can switch the bot to the desired mode. Settings of the bot added to the conversation are independent for each participant. For correct operation, the bot must be given administrator rights.")
            self.pitch = emojize(":check_mark: Pitch change mode selected.\n\nBot will change pitch of any incoming voice message in a random range.")            
            self.recognition = emojize(":check_mark: Voice recognition mode selected.\n\nTo get started, select the language of the messages to be recognized. The following options are available:\n\n:Russia: /r_ru - Russian\n:United_Kingdom: /r_en - English\n:France: /r_fr - French\n:Germany: /r_de - Deutsch\n:Indonesia: /r_id - Indonesian\n:Portugal: /r_pt - Portuguese\n:Spain: /r_es - Spanish\n:India: /r_in - Hindi\n:Turkey: /r_tr - Turkish")            
            self.chosen_lg_to_recognite = emojize("You have chosen a {lang} language for recognition. Bot will try to recognize text of any incoming voice message.")
            self.text_to_speech = emojize(":check_mark: Machine re-sound mode is running. Bot will process any recorded or forwarded voice message.")            
            self.translate_text = emojize(":check_mark: Text translation mode selected.\n\nBot will attempt to translate text of any incoming text message and return translated version.")
            self.changelog = emojize("Soulcatcher 1.2:\n\n:check_mark: Added text translation mode, details with /help\n\n:check_mark: Speech recognition, now available from nine languages. Details with /recognite command.\n\n:check_mark: Support for Russian and English languages for the bot interface. The language automatically adjusts to the user's system language.\n\n:check_mark: Multilingual support for machine re-sound mode.")
            self.processing_audio = "Processing audio..."
            self.empty_v_msg_error = "Voice message does not contain words or the words are not recognized."
            self.translation_proceessing = 'Translation in process...'
            self.languages = {"/r_ru" : "russian", "/r_en" : "english", "/r_fr" : "french", "/r_de" : "deutsch", "/r_id" : "indonesian", "/r_pt" : "portuguese", "/r_es" : "spanish", "/r_in" : "hindi", "/r_tr" : "turkish"}


    def returned(self):
        return self.start

    def return_response(self, response):
        return self.response

def format_translation(translation):               # Формирование переведенного сообщения с флажком страны и текстом.
    print(translation)
    code = translation['code']
    with open('country_codes.json', 'r') as file:
        country_list = json.load(file)
    country_name = country_list[0][code]
    result = ":{country}: {text}".format(country=country_name, text=translation['text'])
    print(country_name)
    return result

def chosen_lg_to_recognite(user_lang, command):                  # Формирование динамического сообщения для выбора языка в распознавателе речи.
    flags = {"/r_ru" : ":Russia:", "/r_en" : ":United_Kingdom:", "/r_fr" : ":France:", "/r_de" : ":Germany:", "/r_id" : ":Indonesia:", "/r_pt" : ":Portugal:", "/r_es" : ":Spain:", "/r_in" : ":India:", "/r_tr" : ":Turkey:"}
    if user_lang == "ru": 
        languages = {"/r_ru" : "русский", "/r_en" : "английский", "/r_fr" : "французский", "/r_de" : "немецкий", "/r_id" : "индонезийский", "/r_pt" : "португальский", "/r_es" : "испанский", "/r_in" : "индийский (хинди)", "/r_tr" : "турецкий"}
        result = emojize("{flag} Для распознавания выбран {lang} язык. Бот попытается распознать текст любого входящего голосового сообщения.".format(flag=flags[command], lang=languages[command]))
    else:
        languages = {"/r_ru" : "russian", "/r_en" : "english", "/r_fr" : "french", "/r_de" : "deutsch", "/r_id" : "indonesian", "/r_pt" : "portuguese", "/r_es" : "spanish", "/r_in" : "hindi", "/r_tr" : "turkish"}
        result = emojize("{flag} The language selected for recognition is {lang}. Bot will try to recognize text of any incoming voice message.".format(flag=flags[command], lang=languages[command]))
    return result

def chose_lg_to_resound(code):
    sup_langs = gtts.lang.tts_langs()
    with open('country_codes.json', 'r') as file:
        country_list = json.load(file)
    country_name = country_list[0][code]
    if code == 'ru':
        message = emojize(":check_mark: Выбран режим машинной переозвучки.\n\nБот попытается распознать текст любого входящего голосового сообщения и вернет машинно переозвученный вариант.\n\n'Анонимность - все, качество - ничто!' (с)\n\nДля продолжения, выберите языкыковой пакет синтезатора речи.\n\n/rs_native - использовать языковой пакет вашей системы для синтеза речи. Бот распознал язык вашей системы как русский :Russia:.\n/rs_english - использовать английский языковой пакет для синтеза речи.")
    elif code == 'en':
        message = emojize(":check_mark: Machine re-sound mode selected.\n\nBot will try to recognize text of any incoming voice message and return a machine re-sounded version.\n\n'Anonymity is everything, quality is nothing!' (с)\n\nTo continue, select speech synthesizer language pack.\n\n/rs_native - Use your system language pack for speech synthesis. Bot recognized your system language as english :{language}:.".format(language=country_name))
    elif code != 'ru' and code in sup_langs:
        message = emojize(":check_mark: Machine re-sound mode selected.\n\nBot will try to recognize text of any incoming voice message and return a machine re-sounded version.\n\n'Anonymity is everything, quality is nothing!' (с)\n\nTo continue, select speech synthesizer language pack.\n\n/rs_native - Use your system language pack for speech synthesis. Bot recognized your system language as :{language}:.\n/rs_english - Use english language pack for speech synthesis.".format(language=country_name))
    elif code != 'ru' and code not in sup_langs:
        message = emojize(":check_mark: Machine re-sound mode selected.\n\nBot will try to recognize text of any incoming voice message and return a machine re-sounded version.\n\n'Anonymity is everything, quality is nothing!' (с)\n\nTo continue, select speech synthesizer language pack.\n\nBot recognized your system language as :{language}:. Unfortunately, this language is not available for speech synthesis. You can try using the package in english.\n/rs_english - Use english language pack for speech synthesis.".format(language=country_name))
    return message
