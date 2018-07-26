# -*- coding: utf-8 -*-
import config
import telebot
from time import sleep
from utypes import BasicUser
from solve import get_answer
from telebot import apihelper


def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("{} [{}]: {}".format(m.chat.first_name,
                                       m.chat.id,
                                       m.text))


bot = telebot.TeleBot(config.token)
bot.set_update_listener(listener)
apihelper.proxy = config.proxy

subject_select = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
for x in list(config.subject_list.keys()):
    subject_select.add(x)
set_select = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
for x in config.command_list[1:]:
    set_select.add('/{}'.format(x))

known_users = {}


@bot.message_handler(commands=[config.command_list[0]])
def command_start(message):
    if message.chat.id not in known_users.keys():
        known_users[message.chat.id] = BasicUser()
    bot.send_message(message.chat.id,
                     'Этот бот поможет вам найти ответы на задания с сайта {}\nКоманда {} устанавливает нужный вам предмет'
                     .format(config.link,
                             config.command_list[2]))
    bot.send_message(message.chat.id,
                     'Выберите предмет',
                     reply_markup=subject_select)
    known_users[message.chat.id].set_step(1)


@bot.message_handler(commands=[config.command_list[2]])
def command_subject(message):
    bot.send_message(message.chat.id,
                     'Выберите предмет',
                     reply_markup=subject_select)
    known_users[message.chat.id].set_step(1)


# TODO: fix crashes on /continue
@bot.message_handler(commands=[config.command_list[1]])
def command_continue(message):
    bot.send_message(message.chat.id,
                     'Введите запрос: ',
                     reply_markup=telebot.types.ForceReply(selective=False))
    known_users[message.chat.id].set_step(2)


@bot.message_handler(func=lambda message: known_users[message.chat.id].get_step() == 1)
def setSubject(message):
    try:
        known_users[message.chat.id].set_subject(config.subject_list[message.text])
        bot.send_message(message.chat.id,
                         'Введите запрос: ',
                         reply_markup=telebot.types.ForceReply(selective=False))
        known_users[message.chat.id].set_step(2)
    except KeyError:
        bot.send_message(message.chat.id,
                         'Выберите предмет из списка.',
                         reply_markup=subject_select)


@bot.message_handler(func=lambda message: known_users[message.chat.id].get_step() == 2)
def communicate(message):
    try:
        bot.send_message(message.chat.id,
                         get_answer(known_users[message.chat.id].get_subject(),
                         message.text))
        known_users[message.chat.id].set_step(0)
        bot.send_message(message.chat.id,
                         'Перейти к выбору предмета?',
                         reply_markup=set_select)
    except Exception as err:
        print("Error occured: {}".format(str(err)))
        bot.send_message(message.chat.id,
                         'Неожиданная ошибка, мы работаем над этим.')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=3)
