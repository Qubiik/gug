"""
 _____
/  __ \
| /  \/ ___  _ __  ___ _   _
| |    / _ \| '_ \/ __| | | |
| \__/\ (_) | | | \__ \ |_| |
 \____/\___/|_| |_|___/\__, |
                        __/ |
                       |___/
©Consy 2024
"""

from random import randint
from telebot import types, TeleBot
from os import listdir
import json
import schedule
import time
import threading
bot = TeleBot("6990833167:AAFR6aZEDl78W5wttJhT84NT1LbyzEQPwRI", parse_mode=None)
admin = "1267002205"
def sendphoto(message):
    files = listdir('neko')
    file_numbers = [int(file.split('.')[0]) for file in files if file.split('.')[0].isdigit()]
    image = open("neko/" + str(randint(0, max(file_numbers))) + ".jpg", "rb")
    bot.send_photo(message.chat.id, image)
    image.close()

db = {}

def job():
    with open("data.json", "w") as fh:
        json.dump(db, fh)

# Запуск планировщика в отдельном потоке
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Планируем выполнение функции каждый час
schedule.every().hour.do(job)

# Запускаем планировщик в отдельном потоке
threading.Thread(target=run_schedule, daemon=True).start()

@bot.message_handler(commands=['neko'])
def neko(message):
    if message.chat.id not in db:
        db[message.chat.id] = {}
        db[message.chat.id]['point'] = 0
    sendphoto(message)
    db[message.chat.id]['point'] += 1

@bot.message_handler(commands=['all_photo'])
def all(message):
    files = listdir("neko")
    file_numbers = [int(file.split('.')[0]) for file in files if file.split('.')[0].isdigit()]
    for i in range(0, max((file_numbers))):
        with open(f"neko/{i}.jpg", "rb") as f:
            bot.send_photo(message.chat.id, f, caption=str(i + 1))
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in db:
        db[message.chat.id] = {}
        db[message.chat.id]['point'] = 0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Neko")
    btn2 = types.KeyboardButton("About")
    btn3 = types.KeyboardButton("Stats")
    markup.add(btn1, btn2, btn3)
    bot.reply_to(message, "Command: \n/neko - send neko image", reply_markup=markup)
@bot.message_handler(commands=['nsfw'])
def nsfw1(message):
    bot.reply_to(message, "/nekoNSFW")
@bot.message_handler(commands=['nekoNSFW'])
def func(message):
    if message.chat.id not in db:
        db[message.chat.id] = {}
        db[message.chat.id]['point'] = 0
    image = open("nsfw/" + str(randint(0, 37)) + ".jpg", "rb")
    bot.send_photo(message.chat.id, image)
    image.close()
    db[message.chat.id]['point'] += 1
@bot.message_handler(content_types=['text'])
def button(message):
    if(message.text == "Neko"):
        sendphoto(message)
        db[message.chat.id]['point'] += 1
    elif(message.text == "About"):
        bot.reply_to(message, "Discord: cons_y\nTelegram: @neko18")
    elif(message.text == "Stats"):
        bot.reply_to(message, f"Nickname: @{message.from_user.username}\nID: {message.from_user.id}\nPoint: {db[message.chat.id]['point']}")
    else:
        try:
            image = open("neko/" + str(int(message.text) - 1) + ".jpg", "rb")
            bot.send_photo(message.chat.id, image)
            image.close()
            db[message.chat.id]['point'] += 1
        except:
            files = listdir('neko')
            file_numbers = [int(file.split('.')[0]) for file in files if file.split('.')[0].isdigit()]
            bot.reply_to(message, f"Максимальное значение {max(file_numbers) + 1}, минимальное значение 1")
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if str(message.chat.id) == admin:
        # Получаем информацию о файле
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_extension = '.' + file_info.file_path.split('.')[-1]

        # Находим порядковый номер для нового файла
        files = listdir('neko')
        file_numbers = [int(file.split('.')[0]) for file in files if file.split('.')[0].isdigit()]
        if file_numbers:
            next_file_number = max(file_numbers) + 1
        else:
            next_file_number = 1

        # Сохраняем файл в папку 'neko'
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'neko/{next_file_number}{file_extension}', 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Фото сохранено!")
bot.polling(none_stop=True)
#alah adbar