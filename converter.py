from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import speech_recognition as sr
from pathlib import Path
from aiogram.types import ContentType, File, Message
from os import path
from pydub import AudioSegment


bot = Bot("5639903354:AAEoYBOskZNYkwpDlFHgQZcYBIJFXDlYh7Y")
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(content_types=[
    types.ContentType.VOICE])
async def record_volume(message: types.Message):

    file_id = message.voice.file_id
    voice = await bot.get_file(message.voice.file_id)
    file_path = voice.file_path
    print(file_path)
    file_on_disk = Path("", f"audio/{file_id}.ogg")
    print(file_on_disk)
    await bot.download_file(file_path, destination=file_on_disk)
    await message.reply(f"Аудио получено, {file_id}")

    sound = AudioSegment.from_ogg(f"audio/{file_id}.ogg")
    sound.export(f"audio/{file_id}.wav", format="wav")

    r = sr.Recognizer()

    AUDIO_FILE = path.join(f"audio/{file_id}.wav")

    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)

    try:
        query = r.recognize_google(audio, language='ru-RU')
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Вы сказали: {query.lower()}')
    except:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ошибка, сообщение не распознано -> попробуйте заново')


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp)
