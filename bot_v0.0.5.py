# -*- coding: utf-8 -*-
import config
import telebot
from time import sleep
from vedis import Vedis
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
for x in config.command_list[1:3]:
    set_select.add('/{}'.format(x))

user_step = Vedis(config.user_step_file)
user_subject = Vedis(config.user_subject_file)

user_step.open()
user_subject.open()

@bot.message_handler(commands=[config.command_list[0]])
def command_start(message):
    if not user_step.exists(message.chat.id):
        with user_step.transaction() and user_subject.transaction():
            user_step[message.chat.id] = 1
            user_subject[message.chat.id] = ''
        get_help(message)
    else:
        bot.send_message(message.chat.id,
                     'Используйте комманду /{}, чтобы получить справку'
                     .format(config.command_list[3]))


@bot.message_handler(commands=[config.command_list[2]])
def command_subject(message):
    bot.send_message(message.chat.id,
                     'Выберите предмет',
                     reply_markup=subject_select)
    with user_step.transaction():
        user_step[message.chat.id] = 1


@bot.message_handler(commands=[config.command_list[1]])
def command_continue(message):
    bot.send_message(message.chat.id,
                     'Введите запрос: ',
                     reply_markup=telebot.types.ForceReply(selective=False))
    with user_step.transaction():
        user_step[message.chat.id] = 2


@bot.message_handler(commands=[config.command_list[3]])
def get_help(message):
    bot.send_message(message.chat.id,
                 'Этот бот поможет вам найти ответы на задания с сайта {}\nКоманда /{} устанавливает нужный вам предмет\nКоманда /{} вызывает справку'
                 .format(config.link,
                         config.command_list[2],
                         config.command_list[3]))
    bot.send_message(message.chat.id,
                     'Выберите предмет',
                     reply_markup=subject_select)


@bot.message_handler(func=lambda message: user_step[message.chat.id].decode() == '1')
def set_subject(message):
    try:
        with user_subject.transaction():
            user_subject[message.chat.id] = config.subject_list[message.text]
        bot.send_message(message.chat.id,
                         'Введите запрос: ',
                         reply_markup=telebot.types.ForceReply(selective=False))
        with user_step.transaction():
            user_step[message.chat.id] = 2
    except KeyError:
        bot.send_message(message.chat.id,
                         'Выберите предмет из списка.',
                         reply_markup=subject_select)


@bot.message_handler(func=lambda message: user_step[message.chat.id].decode() == '2')
def communicate(message):
    try:
        bot.send_message(message.chat.id,
                         get_answer(user_subject[message.chat.id].decode(),
                         message.text))
        with user_step.transaction():
            user_step[message.chat.id] = 0
        bot.send_message(message.chat.id,
                         'Перейти к выбору предмета?',
                         reply_markup=set_select)
    except Exception as err:
        print("Error occured: {}".format(str(err)))
        bot.send_message(message.chat.id,
                         'Неожиданная ошибка, мы работаем над этим.')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=3)
