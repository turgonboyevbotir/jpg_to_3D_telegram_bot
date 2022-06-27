import glob
import shutil
from aiogram import Bot, Dispatcher, executor, types
import pyqrcode
from aiogram.types import ContentType, Message, InputFile
from pathlib import Path
import os
from aiogram.types import InputFile

from triD import jpg_to_3d

bot = Bot(token='5464784479:AAGEf7HAEZQ2cyvAtHY8LRb61KvUUapQ24U')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Hello! ")


@dp.message_handler(commands=['logo'])
async def logo(message: types.Message):
    await message.answer_photo('https://upload.wikimedia.org/wikipedia/commons/9/94/Old_Nike_logo.jpg')


@dp.message_handler(content_types='photo')
async def for_jpg(message: types.Message):
    shutil.rmtree("download/photos")

    download_path = Path().joinpath('download')

    await message.photo[-1].download(destination=download_path)
    global latest_file
    list_of_files = glob.glob(f'download/photos/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    await message.reply(f"{list_of_files}")
    print(list_of_files)
    print(latest_file)
    await bot.send_photo(chat_id=message.chat.id, photo=open(f"{latest_file}", 'rb'))
    jpg_to_3d(latest_file)
    with open("download/photos/blue.stl", 'rb') as a:
        await bot.send_document(chat_id=message.chat.id, document=a)


@dp.message_handler()
async def qr(message: types.Message):
    text = pyqrcode.create(message.text)
    text.png('code.png', scale=5)
    await bot.send_photo(chat_id=message.chat.id, photo=open('code.png', 'rb'))


if __name__ == '__main__':
    executor.start_polling(dp)
