# -*- coding: utf-8 -*-
from requests import get
from bs4 import BeautifulSoup


def get_page(url, data=None):
    req = get(url, data=data)
    soup = BeautifulSoup(req.text, 'lxml')
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()


def format_string(search):
    result = ''
    search = search.replace('\n', ' ').replace('\r', '')
    for i in range(len(search)):
        if search[i] is not ' ' or search[i-1] is not ' ':
            result += search[i]
    return result


def get_excercise(subject, search):
    data = {'search': search}
    url = 'https://{}-ege.sdamgia.ru/search'.format(subject)
    page = get_page(url, data)
    try:
        result = ''
        i = page.index('№') + 2
        while page[i] in '1234567890':
            result += page[i]
            i += 1
    except ValueError:
        result = '-'
    return result


def find_answer(subject, id):
    result = ''
    url = 'https://{}-ege.sdamgia.ru/problem?id={}&print=true'.format(subject, id)
    for i in get_page(url)[::-1]:
        result += i
        if result[-1-len(id):-1] == id[::-1]:
            break
    if len(result) > 100:
        return 'На данный номер ответ не найден'
    return 'Ответ: {}'.format(result[::-1][len(id)+1:])


def get_answer(subject, search):
    id = get_excercise(subject, format_string(search))
    if id is '-':
        return 'Упражнение не найдено...'
    else:
        return '№{}\n{}'.format(id, find_answer(subject, id))
