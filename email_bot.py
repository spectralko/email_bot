import imaplib
import email
import time
import base64
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio

token = "XXXXXX:XXXXX"
bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Начинаю слушать почту")
    while True:
        try:
            server=imaplib.IMAP4_SSL("mail.test.ru", 993)
            server.login('test@test.ru','PWD')
            server.select('INBOX')
            result, data = server.search(None, 'UnSeen')
            ids = data[0]
            id_list = ids.split()
            try:
                latest_email_id = id_list[-1]
                result, data = server.fetch(latest_email_id, "(RFC822)")
                raw_email = email.message_from_bytes(data[0][1])
                if raw_email.is_multipart():
                    for payload in raw_email.get_payload():
                        body_old = payload.get_payload()
                        body = base64.b64decode(body_old.partition('<!D')[0]).decode('utf-8')
                        await bot.send_message(message.chat.id, body)
                else:
                    parse_err = "Произошла ошибка парсера!"
                    await bot.send_message(message.chat.id, parse_err)
            except:
                new_msg = "Новых сообщений нет!"
                print (new_msg)
                #await bot.send_message(message.chat.id, new_msg)
        except:
            conn_err = "Ошибка подключения к серверу!"
            await bot.send_message(message.chat.id, conn_err)
        server.logout()
        time.sleep(61)
if __name__ == '__main__':
    executor.start_polling(dp)
