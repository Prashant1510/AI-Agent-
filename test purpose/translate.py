import asyncio
from googletrans import Translator

async def main():
    translator = Translator()
    result = await translator.translate("Youtube se video downlaod karo", src='auto', dest='en')
    print("Translated:", result.text)

asyncio.run(main())
