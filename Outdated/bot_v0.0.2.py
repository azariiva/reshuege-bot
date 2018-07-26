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
apihelper.proxy = {'https': 'socks5://127.0.0.1:9050'}
bot.set_update_listener(listener)

subjectSelect = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
for x in list(config.subjectList.keys()): subjectSelect.add(x)

setSelect = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
setSelect.add('/setSubject', '/continue')

knownUsers = {}

class User:
    def __init__(self):
        self.step = 0
        self.subject = None

def get_user_step(ID):
    if ID in knownUsers:
        return knownUsers[ID].step
    else:
        knownUsers[ID] = User()
        print("New user detected, who hasn't used \"/start\" yet")
        return 0

def set_user_step(ID, step):
    knownUsers[ID].step = step

def set_user_subject(ID, subject):
    knownUsers[ID].subject = subject

@bot.message_handler(commands=['start'])
def command_start(message):
    if message.chat.id not in knownUsers:
        knownUsers[message.chat.id] = User()

    bot.send_message(message.chat.id, "Этот бот поможет вам найти ответы на задания с сайта https://ege.sdamgia.ru/\nКоманда /setSubject устанавливает нужный вам предмет")
    bot.send_message(message.chat.id, "Выберите предмет", reply_markup=subjectSelect)
    set_user_step(message.chat.id, 1)


@bot.message_handler(commands=['setSubject'])
def command_subject(message):
    bot.send_message(message.chat.id, "Выберите предмет", reply_markup=subjectSelect)
    set_user_step(message.chat.id, 1)

##TODO: fix crashes on /continue
@bot.message_handler(commands=['continue'])
def command_continue(message):
    bot.send_message(message.chat.id, 'Введите запрос: ', reply_markup=telebot.types.ForceReply(selective=False))
    set_user_step(message.chat.id, 2)

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def setSubject(message):
    try:
        set_user_subject(message.chat.id,config.subjectList[message.text])
        bot.send_message(message.chat.id, 'Введите запрос: ', reply_markup=telebot.types.ForceReply(selective=False))
        set_user_step(message.chat.id, 2)
    except KeyError:
        bot.send_message(message.chat.id, 'Выберите предмет из списка.', reply_markup=subjectSelect)

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def communicate(message):
    bot.send_message(message.chat.id, get_answer(knownUsers[message.chat.id].subject, message.text))
    set_user_step(message.chat.id, 0)
    bot.send_message(message.chat.id, "Перейти к выбору предмета?", reply_markup=setSelect)

##TODO: close all dialogs on CTRL+C
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as err:
            print("Error:" + str(err))
            #bot.send_message(message.chat.id, "Неожиданная ошибка, мы работаем над этим.")
        sleep(5)
