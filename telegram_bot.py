import asyncio
import webbrowser
from asyncio import Queue

import httpx
import telebot
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from fastapi import Request, Query
# from telebot import types
# import keyboards as kb
import facebook_auth
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import logging

logging.basicConfig(level=logging.INFO)
my_app_id = '323958937015510'
my_app_secret = '4017320d9d5dcc49869874e73904b872'
fs = facebook_auth.FacebookAuth(my_app_id, my_app_secret, "http://localhost:5000/login/callback", "email")
# bot = telebot.TeleBot("6713056294:AAFAr-2ipWydHjlsiXgKPuxGI-YmeGStvOQ")
greet_kb = ReplyKeyboardMarkup()
bot = Bot(token="6713056294:AAFAr-2ipWydHjlsiXgKPuxGI-YmeGStvOQ")
dp = Dispatcher(bot)
FastAPI = FastAPI
class TelegramBot:
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        kb = [
            [types.KeyboardButton(text="👋 Начать работу с нами")],
            [types.KeyboardButton(text="❓ Узнать подробнее о сервисе")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer("Здравствуйте! Вас приветствует сервис отчетности таргета!", reply_markup=keyboard)

    @dp.message_handler(content_types=['text'])
    async def start_work(message: types.Message):
        if message.text == "👋 Начать работу с нами":
            kb = [
                [types.KeyboardButton(text="Предоставить доступ к своей отчетности Facebook ADS")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer("Нам нужен доступ к вашей отчетности Facebook", reply_markup=keyboard)

        if message.text == "Предоставить доступ к своей отчетности Facebook ADS":
            data_queue = Queue()
            # Помещение данных в очередь в одном потоке
            data_queue.put("05/01/2024")
            # Извлечение данных из очереди в другом потоке
            webbrowser.open('https://localhost:5000/')
            await message.answer("Нам нужен доступ к вашей отчетности Facebook")

    @dp.message_handler(lambda message: message.text.lower() == "Предоставить доступ к своей отчетности Facebook ADS")
    async def facebook(message: types.Message):
        asyncio.create_task(facebook_auth.read_root())
        await message.answer("Нам нужен доступ к вашей отчетности Facebook")


    @dp.message_handler(lambda message: message.text and "❓ Узнать подробнее о сервисе" in message.text.lower())
    async def info(message: types.Message):
        await message.reply("Наш сервис занимается ...")

    def run(self):
        executor.start_polling(dp, skip_updates=True)
    #     @self.bot.message_handler(commands=['start'])
    #     def start(message):
    #         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #         btn1 = types.KeyboardButton("👋 Начать работу с нами")
    #         btn2 = types.KeyboardButton("❓ Узнать подробнее о сервисе")
    #         markup.add(btn1, btn2)
    #         self.bot.send_message(message.chat.id,
    #                               text="Здравствуйте, {0.first_name}! Вас приветствует сервис отчетности таргета".format(
    #                                   message.from_user), reply_markup=markup)
    #
    #     @self.bot.message_handler(content_types=['text'])
    #     def func(message):
    #         back = types.KeyboardButton("Вернуться в главное меню")
    #         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #
    #         if message.text == "👋 Начать работу с нами":
    #             btn1 = types.KeyboardButton("Предоставить доступ к своей отчетности Facebook ADS")
    #             markup.add(btn1)
    #             self.bot.send_message(message.chat.id,
    #                                   text="Уважаемый, {0.first_name}! Нам нужен доступ к вашей отчетности Facebook".format(
    #                                       message.from_user), reply_markup=markup)
    #         elif message.text == "❓ Узнать подробнее о сервисе":
    #             self.bot.send_message(message.chat.id, text="Наш сервис занимается ...")
    #             btn1 = types.KeyboardButton("Как меня зовут?")
    #             btn2 = types.KeyboardButton("Что я могу?")
    #             markup.add(btn1, btn2, back)
    #             self.bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    #         elif message.text == "Предоставить доступ к своей отчетности Facebook ADS":
    #             markup = types.ReplyKeyboardMarkup(row_width=1)
    #             item = types.KeyboardButton("Предоставить доступ к своей отчетности Facebook ADS")
    #             markup.add(item)
    #             btn1 = types.KeyboardButton("Предоставить доступ")
    #             markup.add(btn1)
    #             # Вызываем метод read_root асинхронно
    #             asyncio.create_task(self.facebook_auth.read_root())
    #             self.bot.send_message(message.chat.id, text="перейдите по ссылке: {0.link}".format(self.facebook_auth),
    #                                   reply_markup=markup)
    #
    # async def run(self):
    #     await self.bot.polling(none_stop=True, interval=0)

