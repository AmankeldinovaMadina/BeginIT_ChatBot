import telebot
from telebot import types
import datetime as dt
from openpyxl import load_workbook

bot = telebot.TeleBot('6584233589:AAHMVktC7Ji51ZN_LHqsjnSIss9SK9H2LcE')
dev_id = 6584233589
message_admin = {}
workbook = load_workbook('messages.xlsx')
worksheet = workbook['Sheet1']
count = worksheet.max_row + 1


@bot.message_handler(commands=["start"])
def start(message):
    global count
    chat_id = message.chat.id
    worksheet[f'A{count}'].value = str(dt.datetime.now().date())
    worksheet[f'B{count}'].value = str(dt.datetime.now().time())[0:8]
    worksheet[f'C{count}'].value = f"{message.chat.first_name} {message.chat.last_name}"
    worksheet[f'D{count}'].value = message.chat.username
    
    app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    app_markup.add(types.KeyboardButton('Зарегистрироваться'))
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_sticker(chat_id, sticker=r'CAACAgIAAxkBAAEImRFkO3MzP7AWT8T1uuATaNRRLJav4gACHwADWbv8Jeo5dBvZPTaZLwQ')
    bot.send_message(chat_id, f"Привет {first_name}!\n"
                     f"Welcome to BeginIT!", reply_markup=app_markup)
    
@bot.message_handler(content_types=["text"])
def text(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        if message.text == 'Зарегистрироваться':
            app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            app_markup.add(types.KeyboardButton('Teacher'))
            app_markup.add(types.KeyboardButton('Student'))
            app_markup.add(types.KeyboardButton('Speaker'))

            bot.send_message(chat_id, "Кого вы представляете?", reply_markup=app_markup)
            
            bot.register_next_step_handler(message, select_level)


def send_admin(message):
    global count
    worksheet[f"M{count}"].value = message.text
    count += 1
    workbook.save("messages.xlsx")
    message_admin['partner'] = message.text
    first_name = message.chat.first_name
    chat_id = message.chat.id
    user_name = message.chat.username
    app_name, app_username = [], []
    app_name.append(first_name)
    app_username.append(user_name)
    if message_admin['info'] == 'Нет':
        bot.send_message(admin_id, f"Пришла заявка от {message.chat.first_name}!\n\n"
                                f"Username: {app_username[0]}\n"
                                f"Отправитель: {message_admin['who']}\nУровень: {message_admin['level']}\nКоротко: {message_admin['short_about_event']}\n"
                                f"Дата: {message_admin['date']}\nСсылка: {message_admin['link']}\nОхват: {message_admin['size']}\n"
                                f"Участников: {message_admin['count']}\nПартнеры: {message_admin['partner']}")
    if message_admin['info'] == 'Да':
        bot.send_message(admin_id, f"Пришла заявка!\n\n"
                                f"от: {message.chat.first_name}\n"
                                f"Username: @{app_username[0]}\n"
                                f"Отправитель: {message_admin['who']}\nУровень: {message_admin['level']}\n"
                                f"Партнеры: {message_admin['partner']}")
        
    app_name.clear()
    app_username.clear()
    
    bot.send_message(chat_id, "Поздравляю с успешным прохождением BeginIT", reply_markup=types.ReplyKeyboardRemove())
    
def send_dev(message):
    chat_id = message.chat.id
    bot.send_message(dev_id, f"Поступило сообщение о работе бота!\n\n"
                            f"Текст: {message.text}\n\n"
                            f"Пользователь: {message.chat.first_name}\n"
                            f"Username: @{message.chat.username}")
    bot.send_message(chat_id, f"Ваше сообщение отправлено разработчикам!\nСпасибо за обратную связь 🙏\n\nДля повторного запуска напишите /start")


@bot.message_handler(content_types=["text"])
def select_level(message):
    global count
    worksheet[f"E{count}"].value = message.text
    message_admin['who'] = message.text
    
    chat_id = message.chat.id
    app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    app_markup.add(types.KeyboardButton('Group A'), types.KeyboardButton('Group B'),  types.KeyboardButton('Group C'),  types.KeyboardButton('Group D'))
    bot.send_message(chat_id, "Choose your group 📊:", reply_markup=app_markup)
    message_admin['level'] = message.text
    bot.register_next_step_handler(message, select_info)

@bot.message_handler(content_types=["text"])
def select_info(message):
    global count
    worksheet[f'F{count}'].value = message.text
    message_admin['level'] = message.text
    
    chat_id = message.chat.id
    app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    app_markup.add(types.KeyboardButton('Help'))
    bot.send_message(chat_id, "Задание 1. «Охота за сокровищами»\nЗадание: Исследуйте место, найдите технологические новшества. Создайте в notion фото-коллаж. \nОценка: за отправку коллажа получаете 7 кошкарчиков", reply_markup=app_markup)
    bot.register_next_step_handler(message, select_info_yn)
    message_admin['info'] = message.text

@bot.message_handler(content_types=["document", "text"])
def select_info_yn(message):
    global count
    worksheet[f"G{count}"].value = message.text
    message_admin['info'] = message.text
    
    chat_id = message.chat.id
    if message.text == 'Help':
        bot.send_message(chat_id, "Ответьте на вопросы: Что нового вы увидели для себя? Что удивило? Какие выводы вы сделали для себя? Как это может повлиять на ваш выбор профессии в будущем?", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, event_date)
    else:
        bot.register_next_step_handler(message, event_date)

@bot.message_handler(content_types=["text"])
def event_date(message):
    global count
    worksheet[f"H{count}"].value = message.text
    message_admin['short_about_event'] = message.text
    
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ответьте через чат-бот на вопросы спикера.  ", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, event_link)

@bot.message_handler(content_types=["text"])
def event_link(message):
    global count
    worksheet[f"I{count}"].value = message.text
    message_admin['date'] = message.text
    
    chat_id = message.chat.id
    app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    app_markup.add(types.KeyboardButton('Help'))
    bot.send_message(chat_id, "Задание 6. Провести интервью о сфере IT и профессиях будущего \nУра! Пора начать мини-исследование «5 IT профессий будущего, которые помогут спасти мир». \nОценка по 1 кошкарчику каждому приславшему в оформленный ответ через чат-бот", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, event_size)

@bot.message_handler(content_types=["text"])
def event_size(message):
    global count
    worksheet[f"J{count}"].value = message.text
    message_admin['link'] = message.text
    
    chat_id = message.chat.id
    if message.text == 'Help':
        bot.send_message(chat_id, "Спроси мнения экспертов, участников, собравшихся. Например, можно спросить: Как думаете, насколько информационные технологии будут играть роль в решении глобальных проблем? Какие технологии будут самыми востребованными через 30 лет?Как бы вы назвали эти профессии?Результаты всех наблюдений и интервью напишите, оформите в  notion и загрузите ответ через чат-бот.", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, event_date)
    else:
       bot.send_message(chat_id, "Ответьте через чат-бот на вопросы спикера.", reply_markup=types.ReplyKeyboardRemove())
       bot.register_next_step_handler(message, event_count)

@bot.message_handler(content_types=["text"])
def event_count(message):
    global count
    worksheet[f"K{count}"].value = message.text
    message_admin['size'] = message.text
    
    chat_id = message.chat.id
    app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    app_markup.add(types.KeyboardButton('Выполнить задание'))
    app_markup.add(types.KeyboardButton('Пропустить задание'))
    app_markup.add(types.KeyboardButton('Help'))
    bot.send_message(chat_id, "Задание 7.Питчинг-зона \nА ты помнишь про программы No code и Digital design, которые изучали в BeginIT by inDrive? Задание выполняется по желанию. Можешь запитчить свой проект, и заработать 15 кошкарчиков ", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, select_partner)
    
@bot.message_handler(content_types=["document", "text"])
def select_partner(message):
    global count
    if message_admin['info'] == 'Нет':
        worksheet[f"L{count}"].value = message.text
        message_admin['count'] = message.text
    elif message_admin['info'] == 'Да':
        bot.send_message(admin_id, f"Пришла инфосправка!\n\n"
                                    f"От: {message.chat.first_name}\n"
                                    f"Username: @{message.chat.username}")
        
        try:
            bot.send_document(admin_id, message.document.file_id)
        except:
            bot.send_message(admin_id, 'Упс...😐\nПользователь забыл прикрепить файл')
            
        first_name = message.chat.first_name
        chat_id = message.chat.id
        user_name = message.chat.username
        app_name, app_username = [], []
        app_name.append(first_name)
        app_username.append(user_name)
        app_name.clear()
        app_username.clear()
    
    chat_id = message.chat.id
    app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    app_markup.add(types.KeyboardButton('Help'))
    bot.send_message(chat_id, "Задание 8.Who makes inDrive app? \n Ответьте через чат-бот. \nОценка 1 кошкарчик за вопрос", reply_markup=app_markup)
    message_admin['partner'] = message.text
    bot.register_next_step_handler(message, send_admin)


bot.polling(none_stop=True)