import imaplib
import email
import telebot
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio

token = "XXXXX:XXXXXX"
bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Начинаем слушать почту!")
    while True:
        try:
            server=imaplib.IMAP4_SSL("mail.test.ru", 993)
            server.login('test@test.ru','PWD')
            server.select('INBOX/')
            result, data = server.search(None, 'UnSeen')
            ids = data[0]
            id_list = ids.split()
            latest_email_id = id_list[-1]
            result, data = server.fetch(latest_email_id, "(RFC822)")
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            if email_message.is_multipart():
                for payload in email_message.get_payload():
                    body_old = payload.get_payload()
                    body = body_old.partition('<!D')[0]
                    try:
                        await bot.send_message(message.chat.id, body)
                    except:
                        print ('Что-то поймали!')
            else:
                print("Done")
        except IndexError:
            print ('Новых писем нет!')
        server.logout()
        time.sleep(30)
if __name__ == '__main__':
    executor.start_polling(dp)
