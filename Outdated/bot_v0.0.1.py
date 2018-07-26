# -*- coding: utf-8 -*-

import config
import telebot
from time import sleep
from solve import get_answer
from telebot import apihelper

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

bot = telebot.TeleBot(config.token)
bot.set_update_listener(listener)
apihelper.proxy = config.proxy

subject_select = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
for x in list(config.subject_list.keys()): subject_select.add(x)

set_select = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
set_select.add('/setSubject', '/continue')

known_users = []
user_step = {}
user_subject = {}

def get_user_step(ID):
    if ID in user_step:
        return user_step[ID]
    else:
        known_users.append(ID)
        user_step[ID] = 0
        user_subject[ID] = None
        print("New user detected, who hasn't used \"/start\" yet")
        return 0

@bot.message_handler(commands=['start'])
def command_start(message):

    if message.chat.id not in known_users:
        known_users.append(message.chat.id)
        user_step[message.chat.id] = 0
        user_subject[message.chat.id] = None

    bot.send_message(message.chat.id, """Этот бот поможет вам найти ответы на задания с сайта https://ege.sdamgia.ru/
                                      \nКоманда /setSubject устанавливает нужный вам предмет""")

    bot.send_message(message.chat.id, "Выберите предмет", reply_markup=subject_select)
    user_step[message.chat.id] = 1


@bot.message_handler(commands=['setSubject'])
def command_subject(message):
    bot.send_message(message.chat.id, "Выберите предмет", reply_markup=subject_select)
    user_step[message.chat.id] = 1

@bot.message_handler(commands=['continue'])
def command_continue(message):
    bot.send_message(message.chat.id, 'Введите запрос: ', reply_markup=telebot.types.ForceReply(selective=False))
    user_step[message.chat.id] = 2

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def setSubject(message):
    user_subject[message.chat.id] = config.subject_list[message.text]
    bot.send_message(message.chat.id, 'Введите запрос: ', reply_markup=telebot.types.ForceReply(selective=False))
    user_step[message.chat.id] = 2

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def communicate(message):
    try:
        bot.send_message(message.chat.id, get_answer(user_subject[message.chat.id], message.text))
        user_step[message.chat.id] = 0
        bot.send_message(message.chat.id, "Перейти к выбору предмета?", reply_markup=set_select)

    except Exception as err:
        print("Error occured: " + str(err))
        bot.send_message(message.chat.id, "Неожиданная ошибка, мы работаем над этим.")

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as err:
            print("Error:" + str(err))
    sleep(5)
