import telebot
from telebot import types

# Токен вашего бота
TOKEN = '7193657914:AAEohl5PDJT3fPrukK7-57feBM0DT4zKsI4'
# ID пользователя, которому будут отправляться данные
USER_ID = '6315067215'  # @med_phuket




# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

users = {}

# Функция для отправки анкеты пользователю
def send_survey(user_id):
    survey = "Анкета:\n"
    for question, answer in users[user_id]['answers'].items():
        survey += f"{question}: {answer}\n"
    bot.send_message(USER_ID, survey)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Здравствуйте! Я MEDБOT, я запишу вас на прием к нужному специалисту на Пхукете.")
    bot.send_message(user_id, "Давайте начнем.")
    bot.send_message(user_id, "Кого необходимо записать?",
                     reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                         types.KeyboardButton('Взрослого')).add(types.KeyboardButton('Ребенка')))
    users[user_id] = {'state': 1, 'answers': {}}


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text
    if user_id in users:
        state = users[user_id]['state']
        if state == 1:
            if text == 'Взрослого' or text == 'Ребенка':
                users[user_id]['answers']['Тип пациента'] = text
                users[user_id]['state'] = 2
                bot.send_message(user_id, "Укажите имя и фамилию на английском как в паспорте:")
            else:
                bot.send_message(user_id, "Пожалуйста, выберите вариант из предложенных кнопок.")
        elif state == 2:
            users[user_id]['answers']['Имя и фамилия'] = text
            users[user_id]['state'] = 3
            bot.send_message(user_id, "Укажите дату рождения (день.месяц.год)")
        elif state == 3:
            users[user_id]['answers']['Дата рождения'] = text
            users[user_id]['state'] = 4
            bot.send_message(user_id, "Укажите номер телефона и удобный способ связи (Ватсап, Телеграмм, Инстаграм):")
        elif state == 4:
            users[user_id]['answers']['Контакты'] = text
            users[user_id]['state'] = 5
            bot.send_message(user_id, 'Вы знаете, какой специалист вам нужен?',
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                                 types.KeyboardButton('Да')).add(types.KeyboardButton('Нет')))
        elif state == 5:
            if text == 'Да':
                bot.send_message(user_id, "Выберите специалиста:", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton('Терапевт')).add(types.KeyboardButton('Педиатр')).add(types.KeyboardButton('Окулист(Офтальмолог)')).add(types.KeyboardButton('Хирург')).add(types.KeyboardButton('Невролог')).add(types.KeyboardButton('Гинеколог')).add(types.KeyboardButton('Пластический хирург')).add(types.KeyboardButton('Кардиолог')).add(types.KeyboardButton('Ортопед')).add(types.KeyboardButton('Травматолог')))
            elif text == 'Нет':
                users[user_id]['answers']['Специальность'] = text
                users[user_id]['state'] = 6
                bot.send_message(user_id, "Опишите, какая у вас проблема?",
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                        one_time_keyboard=True).add(
                                     types.KeyboardButton(
                                         'Пройти чекап (ежегодный осмотр, проверить, что все хорошо)')).add(
                                     types.KeyboardButton('Описать жалобы')))
            elif text in ['Терапевт', 'Педиатр', 'Окулист(Офтальмолог)', 'Хирург', 'Невролог', 'Гинеколог', 'Пластический хирург', 'Кардиолог', 'Ортопед', 'Травматолог']:
                users[user_id]['answers']['Специальность'] = text
                users[user_id]['state'] = 6
                bot.send_message(user_id, "Опишите, какая у вас проблема?",
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                        one_time_keyboard=True).add(
                                     types.KeyboardButton(
                                         'Пройти чекап (ежегодный осмотр, проверить, что все хорошо)')).add(
                                     types.KeyboardButton('Описать жалобы')))
        elif state == 6:
            if text == 'Пройти чекап (ежегодный осмотр, проверить, что все хорошо)':
                users[user_id]['answers']['Проблема'] = 'Пройти чек апп( ежегодный осмотр, проверить что все хорошо)'
                users[user_id]['state'] = 7
                bot.send_message(user_id, 'В какой госпиталь/клинику записаться?',
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                        one_time_keyboard=True).add(
                                     types.KeyboardButton(
                                         'Да я знаю(выбрать из списка)')).add(
                                     types.KeyboardButton('Пожалуйста, помогите выбрать')))
            elif text == 'Описать жалобы':
                bot.send_message(user_id, "Опишите вашу проблему:")
            else:
                users[user_id]['answers']['Проблема'] = text
                users[user_id]['state'] = 7
                bot.send_message(user_id, 'В какой госпиталь/клинику записаться?',
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                        one_time_keyboard=True).add(
                                     types.KeyboardButton(
                                         'Да, я знаю')).add(
                                     types.KeyboardButton('Пожалуйста, помогите выбрать'))
                                 )
        elif state == 7:
            if text == 'Да, я знаю':
                bot.send_message(user_id, "Выберите госпиталь/клинику:", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton('Bangkok hospital phuket')).add(types.KeyboardButton('Bangkok Siriroj hospital')).add(types.KeyboardButton('Mission Hospital')).add(types.KeyboardButton('Smart Scan')).add(types.KeyboardButton('Andalab')).add(types.KeyboardButton('Dental Design Phuket Town')).add(types.KeyboardButton('Chiwi clinic')).add(types.KeyboardButton('Lyfe medical Laguna branch')).add(types.KeyboardButton('Lyfe medical Rawai branch')).add(types.KeyboardButton('My Physio by Kannita')).add(types.KeyboardButton('Kathu Dermatology Clinic')))
            elif text in ['Bangkok hospital phuket', 'Bangkok Siriroj hospital', 'Mission Hospital', 'Smart Scan', 'Andalab', 'Dental Design Phuket Town', 'Chiwi clinic', 'Lyfe medical Laguna branch', 'Lyfe medical Rawai branch', 'My Physio by Kannita', 'Kathu Dermatology Clinic']:
                users[user_id]['answers']['Госпиталь'] = text
                users[user_id]['state'] = 8
                bot.send_message(user_id, "Укажите удобное время и дату (например, 01.01.2024 утром/днем/вечером/с … до … /в любое время):")
            else:
                users[user_id]['answers']['Госпиталь'] = text
                users[user_id]['state'] = 8
                bot.send_message(user_id, "Укажите удобное время и дату (например, 01.01.2024 утром/днем/вечером/с … до … /в любое время)")
        elif state == 8:
            users[user_id]['answers']['Время и дата'] = text
            users[user_id]['state'] = 0
            send_survey(user_id)
            bot.send_message(user_id,
                             "Мы успешно приняли заявку на запись, уже связываемся с госпиталем. В отдельных случаях это может занять до 24 часов. Мы постараемся ответить Вам как можно быстрее.",
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                                 types.KeyboardButton('Новая запись')))

    else:
        bot.send_message(user_id, "Пожалуйста, начните с команды /start.")

# Обработчик кнопки "Новая запись"
@bot.message_handler(func=lambda message: message.text == 'Новая запись')
def handle_new_record(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Хорошо, давайте начнем сначала.", reply_markup=types.ReplyKeyboardRemove())
    start(message)

# Запуск бота с бесконечным опросом
bot.infinity_polling()
