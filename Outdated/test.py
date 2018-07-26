import config
import telebot
from telebot import apihelper
from time import sleep

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

bot = telebot.TeleBot(config.token)
apihelper.proxy = {'https': 'socks5://127.0.0.1:9050'}
bot.set_update_listener(listener)

if __name__ == '__main__':
	bot.polling(none_stop = True)
