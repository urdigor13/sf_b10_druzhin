import logging
import requests
import json

from config import *
from aiogram import Bot, Dispatcher, executor, types
from extensions import Convertor, APIException


# Configure logging
#logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Для конвертации валют введите запрос следующего вида:\n<имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>")
@dp.message_handler(commands=['values'])
async def values(message: types.Message):
    text = 'Доступные для расчета валюты валюты: '
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    await message.reply(text)

@dp.message_handler(content_types=['text'])
async def converter(message: types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        await message.reply("Неверное количество параметров!")
    try:
        new_price = Convertor.get_price(base, sym, amount)
        print(new_price)
        await message.reply(f"Цена {amount} {base} в {sym} : {new_price}")
    except APIException as e:
        await message.reply(f"Ошибка в команде:\n{e}")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)