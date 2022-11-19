import translators as ts

async def translate(text, to_language="ru"):
    return ts.google(query_text=text, from_language="auto", to_language=to_language)
