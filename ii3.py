import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

openai.api_key = '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'

bot = Bot("5541458600:AAG0uIvFqorPlBC4dKjX1PxrFBpMvlBQZ1I")
dp = Dispatcher(bot, storage=MemoryStorage())

gf = "how are you"

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="привет")



@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"""
                    Я очень умный бот, отвечающий на вопросы. Если ты задашь мне вопрос, основанный на истине,
                    Я дам вам ответ.
                    Если вы зададите мне вопрос, который является ерундой, обманом или не имеет четкого ответа,
                    Я отвечу \"Unknown\".\n\n
                    Q: Какова продолжительность жизни человека в США?\n
                    A: Средняя продолжительность жизни человека в США составляет 78 лет.\n\n
                    Q: Кто был президентом США в 1955 году?\n
                    A: Дуайт Д. Эйзенхауэр был президентом США в 1955 году.\n\n
                    Q: К какой партии он принадлежал?\n
                    A: Он принадлежал к Республиканской партии.\n\n
                    Q: Чему равен квадратный корень из банана?\n
                    A: Unknown\n\n
                    Q: Как работает телескоп?\n
                    A: В телескопах используются линзы или зеркала, чтобы сфокусировать свет и сделать объекты ближе.\n\n
                    Q: Как играть в футбол?\n
                    A: В футбол играют ногами.\n\n
                    Q: Где проходили Олимпийские игры 1992 года?\n
                    A: Олимпийские игры 1992 года проходили в Барселоне, Испания.\n\n
                    Q: Какой год сейчас?\n
                    A: Сейчас 2023 год\n\n
                    Q: Что ты умеешь?\n
                    A: Если ты задашь мне вопрос, основанный на истине, Я дам вам ответ.\n\n
                    Q: {gf}\n
                    A:""",
        temperature=0.9,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    await message.reply(response["choices"][0]["text"])


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp)