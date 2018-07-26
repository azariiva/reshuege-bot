from bs4 import BeautifulSoup
from requests import get

def get_answer(ID):
    url = 'https://rus-ege.sdamgia.ru/problem?id=' + ID + '&print=true'
    req = get(url, data = None)
    soup = BeautifulSoup(req.text, 'lxml')

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    result = ''
    for i in text[::-1]:
        result += i
        if result[-1-len(ID):-1] == ID[::-1]:
            break
    return result[::-1][len(ID)+1:]

while True:
    ID = input('ID: ')
    print('Ответ:', get_answer(ID))
