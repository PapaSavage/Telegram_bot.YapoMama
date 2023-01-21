from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import speech_recognition as sr
import os
from pathlib import Path
from pydub import AudioSegment

bot = Bot("5815541925:AAFccHSCG0jUjoSr7rgnBH7OmPgrhUBCpVI")
dp = Dispatcher(bot, storage=MemoryStorage())


async def a_to_t(file_id):
    r = sr.Recognizer()

    AUDIO_FILE = os.path.join(f"audio/{file_id}.wav")

    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
    query = r.recognize_google(audio, language='ru-RU')

    # # Удаляем лишние аудиофайлы
    # path = os.path.join(f"audio/{file_id}.wav")
    # os.remove(path)
    # path = os.path.join(f"audio/{file_id}.ogg")
    # os.remove(path)

    return query


async def dest(message):
    file_id = message.voice.file_id
    voice = await bot.get_file(message.voice.file_id)
    file_path = voice.file_path
    file_on_disk = Path("", f"audio/{file_id}.ogg")

    await bot.download_file(file_path, destination=file_on_disk)

    sound = AudioSegment.from_ogg(f"audio/{file_id}.ogg")
    sound.export(f"audio/{file_id}.wav", format="wav")
