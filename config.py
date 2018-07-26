# -*- coding: utf-8 -*-
from os import getcwd

proxy = {'https': 'socks5://127.0.0.1:9050'}

token = '187677466:AAEyQjmAiABebo_aanqNeMipBZKTNKR6378'

link = 'https://ege.sdamgia.ru/'

user_step_file = getcwd() + "\\dbs\\ust.db"
user_subject_file = getcwd() + "\\dbs\\usu.db"

subject_list = {'Русский': 'rus',
                'Математика': 'math',
                'Обществознание': 'soc',
                'История': 'hist',
                'Физика': 'phys',
                'Химия': 'chem',
                'Биология': 'bio'}

command_list = ['start',
                'continue',
                'set_subject',
                'help']
