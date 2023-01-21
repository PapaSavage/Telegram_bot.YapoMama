from converter_audio import a_to_t, dest
from sqlite import db_start, create_profile, edit_profile, create_goods, create_order, search_goods
import openai
from aiogram import Bot, Dispatcher, executor, types
import emoji
from aiogram.types import InlineKeyboardButton,  InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from loader import Start
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from parser_common import pars
import datetime
from datetime import datetime as dt
import random as randomaiz
import requests
import os
from bs4 import BeautifulSoup as BS
import asyncio
import logging
from aiogram.types.message import ContentType


from messages import MESSAGES
from config1 import BOT_TOKEN, PAYMENTS_PROVIDER_TOKEN, TIME_MACHINE_IMAGE_URL


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


openai.api_key = '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'
bot = Bot("5815541925:AAFccHSCG0jUjoSr7rgnBH7OmPgrhUBCpVI")
dp = Dispatcher(bot, storage=MemoryStorage())
loop = asyncio.get_event_loop()

random = set([randomaiz.randint(0, 10) for i in range(3)])
promo = 'Ghsyfhd-5gfsg'
#  ******КЛАВИАТУРЫ*******

# ******Клавиатура buttons(reply_markup = types.ReplyKeyboardRemove() - Выключить клавиатуру)*******
kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True, row_width=2)
b1 = KeyboardButton("Меню")
b2 = KeyboardButton("Корзина")
b3 = KeyboardButton("Заказы")
b4 = KeyboardButton("Помощь")
b5 = KeyboardButton("Рандом")  # Art
kb.add(b1, b2, b3, b4, b5)

# ******Клавиатура inlinebuttons(reply_markup = types.ReplyKeyboardRemove() - Выключить клавиатуру)*******
aa = InlineKeyboardMarkup(row_width=2)
aa1 = InlineKeyboardButton(text='Стоп', callback_data='stop')
aa2 = InlineKeyboardButton(text='Далее', callback_data='Next')
aa.add(aa1, aa2)
#  ******КОНЕЦ_КЛАВИАТУРЫ*******

# Регистрация базы


async def on_startup(_):
    await db_start()
    a = pars("https://yaponomaniya.com/assorty")
    for i in range(len(a)):
        await create_goods(a[i][0], a[i][1], a[i][2], a[i][3], "Сеты")  # Данил

# Чекер на аудио для голосового ввода


async def checker(self):
    if self.text:
        return types.ContentType.TEXT
    if self.audio:
        return types.ContentType.AUDIO
    if self.animation:
        return types.ContentType.ANIMATION
    if self.document:
        return types.ContentType.DOCUMENT
    if self.game:
        return types.ContentType.GAME
    if self.photo:
        return types.ContentType.PHOTO
    if self.sticker:
        return types.ContentType.STICKER
    if self.video:
        return types.ContentType.VIDEO
    if self.video_note:
        return types.ContentType.VIDEO_NOTE
    if self.voice:
        return types.ContentType.VOICE
    if self.contact:
        return types.ContentType.CONTACT
    if self.venue:
        return types.ContentType.VENUE


async def parsing_menu(menu_button):
    req = requests.get(url="https://yaponomaniya.com/")
    html = BS(req.content, 'html.parser')

    for el in html.find_all("li", class_='categories-menu__item'):
        txt = el.find_all("div", class_="categories-menu__item-name")
        menu_button.append(txt[0].text)
    return (menu_button)


async def translate_voice(message: types.Message):
    # print(await content_type(message))
    global user_id
    user_id = message.from_user.id
    file_id = message.voice.file_id
    await dest(message)
    query = await a_to_t(file_id)
    try:
        # Конвертим в текст
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Вы сказали: {query.lower()}')

        path = os.path.join(f"audio/{file_id}.wav")
        os.remove(path)
        path = os.path.join(f"audio/{file_id}.ogg")
        os.remove(path)
        return query
    except:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ошибка, сообщение не распознано -> попробуйте заново')
        return "Ошибка, сообщение не распознано -> попробуйте заново"


async def dick(text_of_audio):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"""
                    Q: Хочу заказать суши\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Хочу заказать суши\n
                    A: Я люблю Пепперони, введи /Sushi для заказа.\n\n
                    Q: Хочу заказать суши\n
                    A: Ко введи /peperoni для заказа.\n\n
                    Q: Какую пиццу ты любишь?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Хочу заказать пепперони\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Какую пиццу мне заказать?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Какую пиццу мне заказать?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Какую пиццу мне заказать?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Какую пиццу мне заказать?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Какую пиццу мне заказать?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: {text_of_audio}\n
                    A:""",
        temperature=0.9,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    await bot.send_message(user_id, text=response["choices"][0]["text"])


async def start_message(message):
    await bot.send_message(chat_id=message.from_user.id, text="Добро пожаловать")


# Setup prices
PRICE = types.LabeledPrice(label='Сет урагимаки', amount=1000)


@dp.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply(MESSAGES['terms'], reply=False)


@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])

    await bot.send_invoice(message.chat.id,
                           title=MESSAGES['tm_title'],
                           description=MESSAGES['tm_description'],
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           photo_url=TIME_MACHINE_IMAGE_URL,
                           photo_height=512,  # !=0/None, иначе изображение не покажется
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICE],
                           start_parameter='time-machine-example',
                           payload='some-invoice-payload-for-our-internal-use'
                           )


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        )
    )


@dp.message_handler(content_types=[
    types.ContentType.VOICE])
async def record_volume(message: types.Message):
    # print(await content_type(message))
    global user_id
    user_id = message.from_user.id
    file_id = message.voice.file_id
    await dest(message)
    query = await a_to_t(file_id)
    try:
        # Конвертим в текст
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Вы сказали: {query.lower()}')
        await dick(query)
        path = os.path.join(f"audio/{file_id}.wav")
        os.remove(path)
        path = os.path.join(f"audio/{file_id}.ogg")
        os.remove(path)

    except:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ошибка, сообщение не распознано -> попробуйте заново')


@dp.message_handler(commands=["start"], state="*")
async def start_command(message: types.Message, state: FSMContext):
    global user_id
    user_id = message.from_user.id
    firstname = message.from_user.first_name
    await bot.send_message(message.from_user.id,
                           text=(
                               f'Добро пожаловать {(emoji.emojize(":ghost:"))}, <b>{firstname}</b>!\nВведите /record чтобы записать свои данные'),
                           reply_markup=kb, parse_mode=types.ParseMode.HTML)
# @dp.message_handler(commands=["Старт"], state = "*")
# @dp.message_handler(commands=["start"], state = Start.start)
# async def start_command(message: types.Message, state: FSMContext):
#     global user_id
#     user_id = message.from_user.id
#     firstname = message.from_user.first_name
#     await bot.send_message(message.from_user.id,
#                            text=(
#                                f'Добро пожаловать {(emoji.emojize(":ghost:"))}, <b>{firstname}</b>!\nВведите /record чтобы записать свои данные'),
#                            reply_markup=kb, parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda message: message.text == "Помощь")
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    global user_id
    user_id = message.from_user.id
    mess = '''/start - начало работы с ботом
           /help - помощь
           /order- сделать заказ
           /random - запустить промоакцию
           /record - Ввести свои данные
           /settings - изменить свои данные
           /buy - чтобы заплатить'''
    await bot.send_message(chat_id=message.from_user.id,
                           text=mess)

# @dp.message_handler(lambda message: message.text == "Рандом", state="*")
# @dp.message_handler(commands=["random"], state="*")
# async def random_command(message: types.Message, state = FSMContext):
#     global user_id
#     user_id = message.from_user.id
#     keyboard = types.InlineKeyboardMarkup()
#     user_data = await state.get_data()
#     try:
#         if user_data["fname_user"] =="Ты уже испытал удачу)":
#             print(user_data["fname_user"])
#             await bot.send_message(chat_id=message.from_user.id ,text="Ты уже испытал удачу)")
#             return 0
#     except:
#         keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
#         await message.answer(f"Сегодня рандомные номера: {random} \n Нажмите на кнопку, чтобы испытать свою удачу", reply_markup=keyboard)
#         await Start.random.set()


@dp.callback_query_handler(text="random_value", state=Start.random)
async def send_random_value(call: types.CallbackQuery, state=FSMContext):
    await state.update_data(fname_user="Ты уже испытал удачу)")
    randpolz = (randomaiz.randint(1, 10))
    if randpolz in random:
        await call.message.answer(f'Вы счастливчик! Вам выпало: {randpolz} \n Мы дарим вам промокод на скидку/бесплатную доставку: ' + promo)
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    else:
        await call.message.answer(f'Вам выпало: {randpolz} \n не расстраивайтесь, приходите завтра за промокодом')
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    await Start.start.set()

# ******Машина состояний1***********


@dp.message_handler(commands=['record', 'settings'], state="*")
async def record_command(message: types.Message, state=FSMContext) -> None:
    global user_id
    user_id = message.from_user.id
    await create_profile(user_id=message.from_user.id)

    await bot.send_message(chat_id=message.from_user.id,
                           text="Мы рады, что вы захотели к нам записаться. Напишите свое имя")

    await Start.name.set()


@dp.message_handler(state=Start.name)
async def name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["name"] = message.text
        name = data["name"]
        await bot.send_message(message.from_user.id,
                               text=f'Спасибо за ответ\nВас зовут: {name}, напишите свой номер телефона')

    await Start.number.set()


@dp.message_handler(state=Start.number)
async def number(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['number'] = message.text
        number = data['number']
        await bot.send_message(message.from_user.id,
                               text=f'Спасибо за ответ\nтвой номер: {number}\nВведите адрес, где бы вы хотели получить заказ')
    await Start.adress.set()


@dp.message_handler(state=Start.adress)
async def adress(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['adress'] = message.text
        await bot.send_message(message.from_user.id,
                               text=f'Данные записаны\n',
                               parse_mode=types.ParseMode.HTML)

    await edit_profile(state, user_id)
    await state.finish()


@dp.message_handler(commands=['order'], state="*")
async def with_puree(message: types.Message, state=FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    menu_button = await parsing_menu([])
    button = [
        [types.InlineKeyboardButton(text=text.strip(), callback_data=text.strip())] for text in menu_button
    ]

    markup.add(*[button for sublist in button for button in sublist])
    await message.answer("что вы хотите заказать?", reply_markup=markup)


@dp.callback_query_handler(text='Сеты', state="*")
# @dp.callback_query_handler(text='Сеты', state = Start.Sets)
async def vt_callback(callback: types.CallbackQuery, state=FSMContext) -> None:
    state.finish()
    markup = types.InlineKeyboardMarkup(row_width=2)
    liste = []
    menu_button = await search_goods()

    button1 = [
        [types.InlineKeyboardButton(text=text[0], callback_data=text[1])] for text in menu_button
    ]
    markup.add(*[button for sublist in button1 for button in sublist])
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=markup)


@dp.callback_query_handler(text='photo/Сет Новогодище АКЦИЯ!.jpg')
async def vt_callback(callback: types.CallbackQuery) -> None:
    aa = InlineKeyboardMarkup(row_width=2)
    aa1 = InlineKeyboardButton(text='Назад', callback_data='Сеты')
    aa2 = InlineKeyboardButton(text='Далее', callback_data='Сеты')
    aa.add(aa1, aa2)

    await callback.message.answer_photo(open("photo/Сет Новогодище АКЦИЯ!.jpg", "rb"), "Филадельфия с форелью слабосоленой, Грин с копченым кальмаром и фирменным кремом с икрой Масаго, Чикен гриль с копченой курицей, Венеция с копченой курицей, Снежный. В сет входит бесплатно: 2 порции васаби, 2 порции имбиря, 2 порции соевого соуса.", reply_markup=aa)


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message, state: FSMContext):
    global user_id
    user_id = message.from_user.id
    if message.text == "ggg":
        return 0
    if message.text == "/peperoni":
        return 0
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"""
                    Q: Помощь\n
                    A: Введите /help или "Помощь" чтобы получить список компанд.\n\n
                    Q: Хочу заказать суши\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Хочу заказать суши\n
                    A: Я люблю Пепперони, введи /Sushi для заказа.\n\n
                    Q: Хочу заказать суши\n
                    A: Ко введи /peperoni для заказа.\n\n
                    Q: Какую пиццу ты любишь?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: Как дела?\n
                    A: У меня всё замечательно.\n\n
                    Q: Как дела?\n
                    A: У меня всё замечательно.\n\n
                    Q: Как дела?\n
                    A: У меня всё замечательно.\n\n
                    Q: Какую пиццу мне заказать?\n
                    A: Я люблю Пепперони, введи /peperoni для заказа.\n\n
                    Q: {message.text}\n
                    A:""",
        temperature=0.9,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    await message.reply(response["choices"][0]["text"])


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=on_startup)
