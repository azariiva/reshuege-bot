from requests import get
from bs4 import BeautifulSoup

def extract(text):
    result = ''

    i = text.index('№') + 2
    while text[i] in '1234567890':
        result += text[i]
        i += 1

    return result

def get_excercise(search):

    data= {'search': search}
    url = 'https://rus-ege.sdamgia.ru/search'

    req = get(url, data = data)
    soup = BeautifulSoup(req.text, 'lxml')
    for script in soup(["script", "style"]):
        script.extract()

    return(extract(soup.get_text()))

print(get_excercise(input()))
